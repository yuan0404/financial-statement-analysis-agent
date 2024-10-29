import fitz
import os
import pytesseract
from PIL import Image
import re

path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = path

pdf_document = "2330.pdf"

output_directory = "output_files"
os.makedirs(output_directory, exist_ok=True)

all_text_filename = os.path.join(output_directory, "2330.txt")
with open(all_text_filename, "w", encoding="utf-8") as all_text_file:
    pass

pdf = fitz.open(pdf_document)

for page_number in range(len(pdf)):
    page = pdf.load_page(page_number)

    text = page.get_text()
    text_filename = os.path.join(output_directory, f"{page_number + 1}.txt")

    with open(text_filename, "w", encoding="utf-8") as text_file:
        text_file.write(text)

    with open(all_text_filename, "a", encoding="utf-8") as all_text_file:
        all_text_file.write(text + "\n")

    images = page.get_images(full=True)
    for img_number, img in enumerate(images, start=1):
        xref = img[0]
        base_image = pdf.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        image_filename = os.path.join(
            output_directory,
            f"{page_number + 1}.{image_ext}"
        )

        with open(image_filename, "wb") as image_file:
            image_file.write(image_bytes)

        image = Image.open(image_filename)
        extracted_text = pytesseract.image_to_string(
            image,
            lang='chi_tra',
            config='--psm 5'
        )

        lines = extracted_text.splitlines()
        lines = [re.sub(r'\s+', ' ', line) for line in lines]
        lines = [re.sub(r'[,.]', '', line) for line in lines]

        with open(text_filename, "a", encoding="utf-8") as text_file:
            text_file.write('\n' + '\n'.join(lines))

        with open(all_text_filename, "a", encoding="utf-8") as all_text_file:
            all_text_file.write('\n' + '\n'.join(lines))

pdf.close()
print("All pages processed.")
