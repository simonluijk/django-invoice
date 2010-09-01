from django.shortcuts import get_object_or_404
from invoice.models import Invoice
from invoice.pdf import draw_pdf
from invoice.utils import pdf_response


def pdf_view(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    file_name = 'Invoice %s.pdf' % invoice.invoice_id
    return pdf_response(draw_pdf, file_name, invoice)
