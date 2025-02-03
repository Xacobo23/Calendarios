from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# from fp.models import FP

# fps = FP.objects.all()

def print_pdf(filename="fps.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Hello World")
    c.save()
    return filename

print_pdf()