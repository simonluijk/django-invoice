from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from invoice.models import Invoice
from invoice.pdf import draw_pdf


def pdf_view(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    filename = 'Invoice-%s.pdf' % invoice.invoice_id
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'inline; filename="%s"' % filename

    draw_pdf(response, invoice)
    return response
