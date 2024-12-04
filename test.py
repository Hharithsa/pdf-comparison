import io
import os
from compare import getTextFromPDF, compareTexts, generateNewPDF

folder_path = "test"  

old_pdf_path = os.path.join(folder_path, "oldPDF_test.pdf")
new_pdf_path = os.path.join(folder_path, "newPDF_test.pdf")

with open(old_pdf_path, "rb") as old_file:
    old_pdf_content = old_file.read()

with open(new_pdf_path, "rb") as new_file:
    new_pdf_content = new_file.read()

old_pdf_stream = io.BytesIO(old_pdf_content)
new_pdf_stream = io.BytesIO(new_pdf_content)

old_pdf_text = getTextFromPDF(old_pdf_stream)
new_pdf_text = getTextFromPDF(new_pdf_stream)

old_text = "\n".join(old_pdf_text)
new_text = "\n".join(new_pdf_text)

diff = compareTexts(old_text, new_text)

diff_pdf = generateNewPDF(diff)

output_pdf_path = os.path.join(folder_path, "output.pdf")

with open(output_pdf_path, "wb") as diff_file:
    diff_file.write(diff_pdf.read())

print(f"New PDF has been generated and saved as '{output_pdf_path}'")
