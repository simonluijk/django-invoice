from invoice.conf import settings

def format_currency(amount):
    return u'%s%.2f %s' % (
        settings.INVOICE_CURRENCY_SYMBOL,
        amount,
        settings.INVOICE_CURRENCY
    )