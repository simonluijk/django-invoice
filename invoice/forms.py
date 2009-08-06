from django import forms
from django.db.models.query import EmptyQuerySet
from django.contrib.auth.models import User
from addressbook.models import Address
from invoice.models import Invoice


class InvoiceAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            address = args[0]['address']
            user = args[0]['user']
            if not address and user:
                args[0]['address'] = User.objects.get(pk=user).get_profile().address.pk
        except IndexError:
            pass

        super(InvoiceAdminForm, self).__init__(*args, **kwargs)

        try:
            addresses = kwargs['instance'].user.get_profile().addresses
        except KeyError:
            try:
                user = int(args[0]['user'])
                addresses = User.objects.get(pk=user).get_profile().addresses
            except (IndexError, ValueError):
                addresses = EmptyQuerySet(model=Address)
        self.fields['address'].queryset = addresses


    class Meta:
        model = Invoice