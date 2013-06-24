#-*- coding:utf-8 -*-
from .conf import settings


def invoice(request):
    return {
        "INV_CURRENCY": settings.INV_CURRENCY,
        "INV_CURRENCY_SYMBOL": settings.INV_CURRENCY_SYMBOL,
    }
