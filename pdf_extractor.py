import fitz


def extract_text_from_pdf(pdf_file):
    try:
        document = fitz.open(stream=pdf_file.read(), filetype="pdf")

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        if not text.strip():
            raise ValueError("No readable text was found in this PDF.")

        return text

    except Exception as e:
        raise ValueError(f"Could not extract PDF text: {e}")
