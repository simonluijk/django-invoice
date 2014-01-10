Django Invoice
==============

**Create invoices on your django website.**

[![build-status]][travis]

# Overview

Django-invoice is a little Django app that allows you to create invoices in
a Django project.

# Requirements

* Python (2.6, 2.7)
* Django (1.5, 1.6)
* django-addresses

# Installation

Install using `pip`...

    pip install django-invoice

# Setup

Add it to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'invoice',
        'addressbook',
    )

Create user profile model with an addresses foreign key to Address. I normally
put this in an account app. Don't forget to add it to your `INSTALLED_APPS`.

    from django.db import models
    from django.contrib.auth.models import User

    from addressbook.models import Address


    class UserProfile(models.Model):
        user = models.ForeignKey(User, unique=True)
        addresses = models.ManyToManyField(Address)

        def __unicode__(self):
            return self.user.email

        @property
        def address(self):
            return self.addresses.latest()

Set the model as your auth profile model.

    AUTH_PROFILE_MODULE = 'account.UserProfile'

Run `python manage.py syncdb --migrate`.

Configure your settings. Apart from `INV_MODULE` they are self explanatory.
`INV_MODULE` is a path to a module that contains functions to customize the
invoice.

    INV_MODULE = 'invoice_mod'
    INV_CURRENCY = u'EUR'
    INV_CURRENCY_SYMBOL = u'€'
    INV_LOGO = 'static/images/logo.jpg'

Here is an example module to customize the invoice.

    from reportlab.lib.units import cm
    from invoice.conf import settings


    business_details = (
        u'Your Name',
        u'# A street',
        u'##### Town',
        u'Country',
        u'',
        u'Email: you@example.com',
        u'Site: www.example.com',
        u'Tel: 0## ### ### ###'
    )

    note = (
        u'PAYMENT TERMS: 30 DAYS FROM INVOICE DATE.',
        u'Please make all cheques payable to Your Name.',
    )


    def draw_header(canvas):
        """ Draws the invoice header """
        canvas.setStrokeColorRGB(0.13, 0.55, 0.87)
        canvas.setFillColorRGB(0.2, 0.2, 0.2)
        canvas.setFont('Helvetica', 16)
        canvas.drawString(18 * cm, -1 * cm, 'Invoice')
        canvas.drawInlineImage(settings.INV_LOGO, 1 * cm, -1 * cm, 92, 16)
        canvas.setLineWidth(4)
        canvas.line(0, -1.25 * cm, 21.7 * cm, -1.25 * cm)


    def draw_address(canvas):
        """ Draws the business address """
        canvas.setFont('Helvetica', 9)
        textobject = canvas.beginText(13 * cm, -2.5 * cm)
        for line in business_details:
            textobject.textLine(line)
        canvas.drawText(textobject)


    def draw_footer(canvas):
        """ Draws the invoice footer """
        textobject = canvas.beginText(1 * cm, -27 * cm)
        for line in note:
            textobject.textLine(line)
        canvas.drawText(textobject)

That's it, we're done!

# Going forward

Here is a list of things that need to be improved. If you wish to help please
submit a pull request or open an issue. It is a small project so should be
easy to picked up.

* Remove the need for a user profile.
* Recurring invoice support.
* Replace current invoice customization with something new.
* Improve documentation.
* Improve test coverage.

[build-status]: https://travis-ci.org/simonluijk/django-invoice.png?branch=master
[travis]: http://travis-ci.org/simonluijk/django-invoice?branch=master
