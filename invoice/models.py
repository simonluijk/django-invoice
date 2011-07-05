from datetime import date
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django_extensions.db.models import TimeStampedModel

from addressbook.models import Address
from invoice.utils import format_currency, friendly_id


class InvoiceManager(models.Manager):
    def get_due(self):
        return self.filter(invoice_date__lte=date.today(),
                           invoiced=False,
                           draft=False)

class Invoice(TimeStampedModel):
    user = models.ForeignKey(User)
    address = models.ForeignKey(Address, related_name='%(class)s_set')
    invoice_id = models.CharField(max_length=6, null=True, blank=True, unique=True, editable=False)
    invoice_date = models.DateField(default=date.today)
    invoiced = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)

    objects = InvoiceManager()

    def __unicode__(self):
        return u'%s (%s)' % (self.invoice_id, self.total_amount())

    def total_amount(self):
        return format_currency(self.total())

    def total(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total = total + item.total()
        return total

    def file_name(self):
        return u'Invoice %s.pdf' % self.invoice_id

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

    class Meta:
        ordering = ('-invoice_date', 'id')


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', unique=False)
    description = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=1)

    def total(self):
        return Decimal(str(self.unit_price * self.quantity)).quantize(Decimal('0.01'))

    def __unicode__(self):
        return self.description

