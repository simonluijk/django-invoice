from datetime import date
from decimal import Decimal
from StringIO import StringIO
from email.mime.application import MIMEApplication

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from django.template.loader import render_to_string, get_template
from django.template import TemplateDoesNotExist, Context
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from addressbook.models import Address
from .utils import format_currency, friendly_id
from .conf import settings as app_settings
from .pdf import draw_pdf


class Currency(models.Model):
    code = models.CharField(unique=True, max_length=3)
    pre_symbol = models.CharField(blank=True, max_length=1)
    post_symbol = models.CharField(blank=True, max_length=1)

    def __unicode__(self):
        return self.code


class InvoiceManager(models.Manager):
    def get_invoiced(self):
        return self.filter(invoiced=True, draft=False)

    def get_due(self):
        return self.filter(invoice_date__lte=date.today(),
                           invoiced=False,
                           draft=False)


class Invoice(TimeStampedModel):
    user = models.ForeignKey(User)
    currency = models.ForeignKey(Currency, blank=True, null=True)
    address = models.ForeignKey(Address, related_name='%(class)s_set')
    invoice_id = models.CharField(unique=True, max_length=6, null=True,
                                  blank=True, editable=False)
    invoice_date = models.DateField(default=date.today)
    invoiced = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)

    objects = InvoiceManager()

    def __unicode__(self):
        return u'%s (%s)' % (self.invoice_id, self.total_amount())

    class Meta:
        ordering = ('-invoice_date', 'id')

    def save(self, *args, **kwargs):
        try:
            self.address
        except Address.DoesNotExist:
            try:
                self.address = self.user.get_profile().address
            except User.DoesNotExist:
                pass

        super(Invoice, self).save(*args, **kwargs)

        if not self.invoice_id:
            self.invoice_id = friendly_id.encode(self.pk)
            kwargs['force_insert'] = False
            super(Invoice, self).save(*args, **kwargs)

    def total_amount(self):
        return format_currency(self.total(), self.currency)

    def total(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total = total + item.total()
        return total

    def file_name(self):
        return u'Invoice %s.pdf' % self.invoice_id

    def send_invoice(self):
        pdf = StringIO()
        draw_pdf(pdf, self)
        pdf.seek(0)

        attachment = MIMEApplication(pdf.read())
        attachment.add_header("Content-Disposition", "attachment",
                              filename=self.file_name())
        pdf.close()

        subject = app_settings.INV_EMAIL_SUBJECT % {"invoice_id": self.invoice_id}
        email_kwargs = {
            "invoice": self,
            "SITE_NAME": settings.SITE_NAME,
            "INV_CURRENCY": app_settings.INV_CURRENCY,
            "INV_CURRENCY_SYMBOL": app_settings.INV_CURRENCY_SYMBOL,
            "SUPPORT_EMAIL": settings.MANAGERS[0][1],
        }
        try:
            template = get_template("invoice/invoice_email.html")
            body = template.render(Context(email_kwargs))
        except TemplateDoesNotExist:
            body = render_to_string("invoice/invoice_email.txt", email_kwargs)
        email = EmailMultiAlternatives(subject=subject, body=strip_tags(body), to=[self.user.email])
        email.attach_alternative(body, "text/html")
        email.attach(attachment)
        email.send()

        self.invoiced = True
        self.save()


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', unique=False)
    description = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=1)

    def total(self):
        total = Decimal(str(self.unit_price * self.quantity))
        return total.quantize(Decimal('0.01'))

    def __unicode__(self):
        return self.description
