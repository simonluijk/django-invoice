from django.http import HttpResponse
from ..conf import settings


def format_currency(amount, currency):
    if currency:
        return u"{1.pre_symbol} {0:.2f} {1.post_symbol} {1}".format(amount, currency)

    return u"%s %.2f %s" % (
        settings.INV_CURRENCY_SYMBOL, amount, settings.INV_CURRENCY
    )


def pdf_response(draw_funk, file_name, *args, **kwargs):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=\"%s\"" % file_name
    draw_funk(response, *args, **kwargs)
    return response


def send_invoices():
    from ..models import Invoice

    for invoice in Invoice.objects.get_due():
        invoice.send_email()
