from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image

import csv
import os


def import_data():
    #inv_data = csv.reader(open(data_file, "r"))
    inv_data = ('alx','alx','alx','alx','alx','alx','alx','alx','alx','alx','alx','alx')
    for row in inv_data:
        var1 = row[0]
        # do more stuff

        #pdf_file = os.path.abspath("~/Desktop/%s.pdf" % var1)
        #generate_pdf(variable, pdf_file)
        pdf_name = '0000' + ".pdf"
        save_name = os.path.join(os.path.expanduser("~"), "Desktop/", pdf_name)

        c = canvas.Canvas(save_name, pagesize=letter)
        # do some stuff with my variables
        c.setFont("Helvetica", 40, leading=None)
        c.drawString(150, 2300, var1)
        c.showPage()
        c.save()

def generate_pdf(variable, file_name):

    c = canvas.Canvas(file_name, pagesize=letter)

    # do some stuff with my variables
    c.setFont("Helvetica", 40, leading=None)
    c.drawString(150, 2300, var1)

    c.showPage()
    c.save()

import_data()