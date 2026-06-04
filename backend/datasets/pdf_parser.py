import requests
import pdfplumber
import io


def extract_text_from_pdf(pdf_url):

    response = requests.get(pdf_url)

    pdf_file = io.BytesIO(response.content)

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text