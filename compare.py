from difflib import ndiff
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

import fitz 
import re

def getTextFromPDF(file):
    doc = fitz.open(stream=file, filetype="pdf")
    textBlocks = []
    for pageNum in range(doc.page_count):
        page = doc.load_page(pageNum)
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if 'lines' in block:
                blockText = []
                for line in block['lines']:
                    lineText = ''.join([span['text'] for span in line['spans']]).strip()
                    if lineText:
                        blockText.append(lineText)
                textBlocks.append('\n'.join(blockText))
    return textBlocks

def preprocessText(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    if not text:
        return ''
    return text

def compareTexts(textA, textB):
    textA = "\n".join([line for line in (preprocessText(line) for line in textA.splitlines()) if line != ''])
    textB = "\n".join([line for line in (preprocessText(line) for line in textB.splitlines()) if line != ''])
    diff = list(ndiff(textA.splitlines(), textB.splitlines()))
    return diff

def generateNewPDF(diff):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    y_position = 750
    line_height = 12

    for line in diff:
        if y_position < 50:
            c.showPage()
            y_position = 750
        
        if line.startswith('+'):
            c.setFillColorRGB(0, 1, 0)
            text = line[2:]
        elif line.startswith('-'):
            c.setFillColorRGB(1, 0, 0)
            text = line[2:]
        elif line.startswith(' '):
            c.setFillColorRGB(0, 0, 0)
            text = line[2:]
        else:
            continue
        
        c.drawString(30, y_position, text)
        y_position -= line_height
    
    c.save()
    packet.seek(0)
    return packet
