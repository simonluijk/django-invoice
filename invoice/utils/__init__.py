from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings as dsettings
from email.mime.application import MIMEApplication
from datetime import date
from StringIO import StringIO

from ..conf import settings


def format_currency(amount):
    return u"%s %.2f %s" % (
        settings.INV_CURRENCY_SYMBOL, amount, settings.INV_CURRENCY
    )


def pdf_response(draw_funk, file_name, *args, **kwargs):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename='%s'" % file_name
    draw_funk(response, *args, **kwargs)
    return response


def send_invoices():
    from ..models import Invoice
    from ..pdf import draw_pdf

    for invoice in Invoice.objects.filter(invoice_date__lte=date.today(), invoiced=False):
        pdf = StringIO()
        draw_pdf(pdf, invoice)
        pdf.seek(0)

        attachment = MIMEApplication(pdf.read())
        attachment.add_header("Content-Disposition", "attachment", filename=invoice.file_name())
        pdf.close()

        subject = settings.INV_EMAIL_SUBJECT % {"invoice_id": invoice.invoice_id}
        email = EmailMessage(subject=subject, to=[invoice.user.email])
        email.body = render_to_string("invoice/invoice_email.txt", {
            "invoice": invoice,
            "SITE_NAME": dsettings.SITE_NAME,
            "INV_CURRENCY": settings.INV_CURRENCY,
            "INV_CURRENCY_SYMBOL": settings.INV_CURRENCY_SYMBOL,
            "SUPPORT_EMAIL": dsettings.MANAGERS[0][1],
        })
        email.attach(attachment)
        email.send()

        invoice.invoiced = True
        invoice.save()

