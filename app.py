import streamlit as st

from pdf_extractor import extract_text_from_pdf


st.set_page_config(
    page_title="AI Research Dataset Extractor",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Research Dataset Extractor")

st.write(
    "Upload a research paper PDF to extract its text."
)


uploaded_file = st.file_uploader(
    "Upload Research Paper",
    type=["pdf"]
)


if uploaded_file is not None:

    st.info(f"File uploaded: {uploaded_file.name}")

    try:
        extracted_text = extract_text_from_pdf(uploaded_file)

        st.success("PDF text extracted successfully!")

        st.subheader("Extracted Text")

        st.text_area(
            "Paper Content",
            extracted_text,
            height=500
        )

    except ValueError as e:

        st.error(str(e))

    except Exception as e:

        st.error(f"Unexpected error: {e}")
