# utils.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_invoice_pdf(invoice):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, f"Invoice #{invoice.invoice_number}")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 780, f"Customer: {invoice.customer_email}")
    c.drawString(100, 760, f"Date: {invoice.created_at.strftime('%Y-%m-%d')}")
    c.drawString(100, 740, f"Total Amount: ${invoice.total_amount}")

    # Table for items
    y = 700
    c.setFont("Helvetica-Bold", 10)
    c.drawString(100, y, "Item")
    c.drawString(300, y, "Quantity")
    c.drawString(400, y, "Price")
    
    c.setFont("Helvetica", 10)
    for item in invoice.items.all():
        y -= 20
        c.drawString(100, y, item.product_name)
        c.drawString(300, y, str(item.quantity))
        c.drawString(400, y, f"${item.price}")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
