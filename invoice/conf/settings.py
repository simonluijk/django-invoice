# -*- coding: UTF-8 -*-
from os import path
from django.conf import settings

try:
    INVOICE_LOGO = settings.INVOICE_LOGO
except AttributeError:
    INVOICE_LOGO = path.join(settings.MEDIA_ROOT, 'static/images/logo.png')

try:
    INVOICE_CURRENCY = settings.INVOICE_CURRENCY
except AttributeError:
    INVOICE_CURRENCY = 'EUR'

try:
    INVOICE_CURRENCY_SYMBOL = settings.INVOICE_CURRENCY_SYMBOL
except AttributeError:
    INVOICE_CURRENCY_SYMBOL = '€'

try:
    INVOICE_NOTE = settings.INVOICE_NOTE
except AttributeError:
    INVOICE_NOTE = (
        'Please make all cheques payable to __________________.',
    )

try:
    INVOICE_BUSINESS = settings.INVOICE_BUSINESS
except AttributeError:
    INVOICE_BUSINESS = (
        'Your address',
        '',
        'and contact',
        'details goes',
        'here.'
    )