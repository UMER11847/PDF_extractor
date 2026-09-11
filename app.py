import streamlit as st

from pdf_extractor import extract_text_from_pdf
from llm_extractor import extract_dataset_metadata


st.set_page_config(
    page_title="AI Research Dataset Extractor",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Research Dataset Extractor")

st.write(
    "Upload a research paper PDF to extract structured dataset information."
)


uploaded_file = st.file_uploader(
    "Upload Research Paper",
    type=["pdf"]
)


if uploaded_file is not None:

    st.info(f"File uploaded: {uploaded_file.name}")

    try:

        # -----------------------------
        # STEP 1: Extract PDF text
        # -----------------------------

        extracted_text = extract_text_from_pdf(uploaded_file)

        st.success("PDF text extracted successfully!")

        with st.expander("📄 View Extracted Paper Text"):

            st.text_area(
                "Paper Content",
                extracted_text,
                height=400
            )


        # -----------------------------
        # STEP 2: Send to Gemini
        # -----------------------------

        if st.button("🤖 Extract Dataset Information"):

            with st.spinner(
                "Gemini is analyzing the research paper..."
            ):

                metadata = extract_dataset_metadata(
                    extracted_text
                )


            st.success(
                f"Successfully extracted {len(metadata)} dataset(s)!"
            )


            # -----------------------------
            # STEP 3: Display datasets
            # -----------------------------

            st.subheader("📊 Extracted Dataset Information")


            for index, dataset in enumerate(metadata):

                st.markdown(
                    f"### Dataset {index + 1}"
                )

                data = dataset.model_dump()


                # Dataset name
                st.write(
                    "**Dataset Name:**",
                    data.get("dataset_name")
                )


                # Dataset details
                if data.get("dataset_details"):

                    st.write("**Dataset Details:**")

                    st.json(
                        data["dataset_details"]
                    )


                # Data types
                if data.get("data_types"):

                    st.write("**Data Types:**")

                    for item in data["data_types"]:

                        st.write(
                            f"- {item}"
                        )


                # Modalities
                if data.get("modalities"):

                    st.write("**Modalities:**")

                    for item in data["modalities"]:

                        st.write(
                            f"- {item}"
                        )


                # Tasks
                if data.get("tasks"):

                    st.write("**Tasks:**")

                    for item in data["tasks"]:

                        st.write(
                            f"- {item}"
                        )


                # License
                st.write(
                    "**License:**",
                    data.get("licensing_information")
                )


                # URL
                st.write(
                    "**Source URL:**",
                    data.get("source_url")
                )


                # Full JSON
                with st.expander(
                    "View JSON"
                ):

                    st.json(data)


                st.divider()


    except ValueError as e:

        st.error(str(e))


    except Exception as e:

        st.error(
            f"Unexpected error: {e}"
        )
