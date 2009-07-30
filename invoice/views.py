from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from invoice.conf import settings
from invoice.models import Invoice
from invoice.utils.format import format_currency


def pdf_view(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    # Init response
    filename = 'Invoice-%s.pdf' % invoice.invoice_id
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'inline; filename="%s"' % filename

    # Create canvas
    cnv = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Set colours
    cnv.setStrokeColorRGB(0.9, 0.5, 0.2)
    cnv.setFillColorRGB(0.2, 0.2, 0.2)

    # Title
    cnv.translate(0.5*cm, height-1*cm)
    cnv.setFont('Helvetica', 16)
    cnv.drawString(width-3*cm, 0, 'Invoice')
    cnv.drawInlineImage(settings.INVOICE_LOGO, 0, 0, 250, 16)
    cnv.setLineWidth(4)
    cnv.line(-0.5*cm, -0.25*cm, width, -0.25*cm)

    # Change font
    cnv.setFont('Helvetica', 10)
    cnv.translate(0.5*cm, -1.5*cm)

    # Client address
    textobject = cnv.beginText()
    if invoice.address.contact_name:
        textobject.textLine(invoice.address.contact_name)
    textobject.textLine(invoice.address.address_one)
    if invoice.address.address_two:
        textobject.textLine(invoice.address.address_two)
    textobject.textLine(invoice.address.town)
    if invoice.address.county:
        textobject.textLine(invoice.address.county)
    textobject.textLine(invoice.address.postcode)
    textobject.textLine(invoice.address.country.name)
    cnv.drawText(textobject)

    # Business address
    textobject = cnv.beginText()
    textobject.setTextOrigin(width-width/2, 0)
    for line in settings.INVOICE_BUSINESS:
        textobject.textLine(line)
    cnv.drawText(textobject)

    # Info
    cnv.translate(0, -4*cm)
    textobject = cnv.beginText()
    textobject.textLine(u'Invoice ID: %s' % invoice.invoice_id)
    textobject.textLine(u'Invoice Date: %s' % invoice.invoice_date.strftime('%d %b %Y'))
    textobject.textLine(u'Client: %s' % invoice.user.username)
    cnv.drawText(textobject)

    # Items
    data=  [[u'Quantity', u'Description', u'Amount', u'Total'],]
    for item in invoice.items.all():
        data.append([
            item.quantity,
            item.description,
            format_currency(item.unit_price),
            format_currency(item.total())
        ])
    data.append([u'', u'', u'Total:', format_currency(invoice.total())])
    table = Table(data,
        style=[
            ('FONT', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('TEXTCOLOR', (0,0), (-1,-1), (0.2, 0.2, 0.2)),
            ('GRID', (0,0), (-1,-2), 1, (0.7, 0.7, 0.7)),
            ('GRID', (-2,-1), (-1,-1), 1, (0.7, 0.7, 0.7)),
            ('ALIGN', (-2,0), (-1,-1), 'RIGHT'),
            ('BACKGROUND', (0,0), (-1,0), (0.8, 0.8, 0.8)),
        ],
        colWidths=[2*cm, 11*cm, 3*cm, 3*cm]
    )
    tw, th = table.wrapOn(cnv, 15*cm, 19*cm)
    table.drawOn(cnv, 0, -2*cm-th)

    # Instructions
    cnv.translate(0, -3*cm-th)
    textobject = cnv.beginText()
    for line in settings.INVOICE_NOTE:
        textobject.textLine(line)
    cnv.drawText(textobject)

    cnv.showPage()
    cnv.save()
    return response