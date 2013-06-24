from django.contrib import admin
from django.conf.urls import patterns
from invoice.models import Invoice, InvoiceItem, Currency
from invoice.views import pdf_view
from invoice.forms import InvoiceAdminForm


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline, ]
    fieldsets = (
        (None, {
            'fields': ('user', 'address', 'invoice_date', 'paid_date', 'draft', 'currency')
        }),
    )
    search_fields = ('invoice_id', 'user__username')
    list_display = (
        'invoice_id',
        'total_amount',
        'user',
        'draft',
        'invoice_date',
        'invoiced',
        'paid_date',
    )
    form = InvoiceAdminForm
    actions = ['send_invoice', ]

    def get_urls(self):
        urls = super(InvoiceAdmin, self).get_urls()
        wrapped_pdf_view = self.admin_site.admin_view(pdf_view)
        return patterns('', (r'^(.+)/pdf/$', wrapped_pdf_view)) + urls

    def send_invoice(self, request, queryset):
        for invoice in queryset.all():
            invoice.send_invoice()

    send_invoice.short_description = "Send invoice to client"


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Currency)
