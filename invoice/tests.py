import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from addressbook.models import Address, Country

from .models import Invoice


class InvoiceTestCase(TestCase):
    def setUp(self):
        usr = User.objects.create(username='test',
                                  first_name='John',
                                  last_name='Doe',
                                  email='example@example.com')

        country = Country.objects.create(name='TestCountry')
        address = Address.objects.create(contact_name='John Doe',
                                         address_one='Street',
                                         town='Town',
                                         postcode='PostCode',
                                         country=country)

        self.inv = Invoice.objects.create(user=usr, address=address)

    def testInvoiceId(self):
        inv = self.inv
        self.assertEquals(inv.invoice_id, u'TTH9R')

        inv.invoice_id = False
        inv.save()

        self.assertEquals(inv.invoice_id, u'TTH9R')

    def testGetDue(self):
        inv = self.inv

        inv.draft = True
        inv.save()
        self.assertEquals(len(Invoice.objects.get_due()), 0)

        inv.draft = False
        inv.save()
        self.assertEquals(len(Invoice.objects.get_due()), 1)

        inv.invoiced = True
        inv.save()
        self.assertEquals(len(Invoice.objects.get_due()), 0)

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(1)
        tomorrow = today + datetime.timedelta(1)

        inv.invoiced = False
        inv.invoice_date = yesterday
        inv.save()
        self.assertEquals(len(Invoice.objects.get_due()), 1)

        inv.invoice_date = tomorrow
        inv.save()
        self.assertEquals(len(Invoice.objects.get_due()), 0)
