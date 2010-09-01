from invoice.conf import settings


def format_currency(amount):
    return u'%s %.2f %s' % (
        settings.INV_CURRENCY_SYMBOL, amount, settings.INV_CURRENCY
    )
