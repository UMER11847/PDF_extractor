import streamlit as st
import json
import pandas as pd

from pdf_extractor import extract_text_from_pdf
from llm_extractor import extract_dataset_metadata
from database import create_database, save_dataset


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Research Dataset Extractor",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

create_database()


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📄 AI Research Dataset Extractor")

st.write(
    "Upload a research paper PDF to extract structured dataset information "
    "using AI."
)


# --------------------------------------------------
# PDF UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Research Paper",
    type=["pdf"]
)


# --------------------------------------------------
# PROCESS PDF
# --------------------------------------------------

if uploaded_file is not None:

    st.info(f"File uploaded: {uploaded_file.name}")

    try:

        # Extract text from PDF
        extracted_text = extract_text_from_pdf(uploaded_file)

        st.success("PDF text extracted successfully!")


        # --------------------------------------------------
        # SHOW EXTRACTED TEXT
        # --------------------------------------------------

        with st.expander("📄 View Extracted Paper Text"):

            st.text_area(
                "Paper Content",
                extracted_text,
                height=400
            )


        # --------------------------------------------------
        # EXTRACT DATASET INFORMATION
        # --------------------------------------------------

        if st.button("🤖 Extract Dataset Information"):

            with st.spinner(
                "Gemini is analyzing the research paper..."
            ):

                metadata = extract_dataset_metadata(
                    extracted_text
                )


            # Store metadata in session state
            st.session_state["metadata"] = metadata

            st.success(
                "Dataset information extracted successfully!"
            )


        # --------------------------------------------------
        # HUMAN REVIEW SECTION
        # --------------------------------------------------

        if "metadata" in st.session_state:

            st.subheader("🔍 Review Extracted Dataset Information")

            st.write(
                "Review and edit the information before saving it."
            )


            reviewed_datasets = []


            for index, dataset in enumerate(
                st.session_state["metadata"]
            ):

                st.markdown(
                    f"### Dataset {index + 1}"
                )


                # Convert Pydantic model to dictionary
                data = dataset.model_dump()


                # --------------------------------------------------
                # DATASET NAME
                # --------------------------------------------------

                dataset_name = st.text_input(
                    "Dataset Name",
                    value=data.get("dataset_name") or "",
                    key=f"dataset_name_{index}"
                )


                # --------------------------------------------------
                # DATA TYPES
                # --------------------------------------------------

                existing_data_types = data.get(
                    "data_types"
                ) or []


                data_types = st.text_input(
                    "Data Types (comma separated)",
                    value=", ".join(existing_data_types),
                    key=f"data_types_{index}"
                )


                # --------------------------------------------------
                # MODALITIES
                # --------------------------------------------------

                existing_modalities = data.get(
                    "modalities"
                ) or []


                modalities = st.text_input(
                    "Modalities (comma separated)",
                    value=", ".join(existing_modalities),
                    key=f"modalities_{index}"
                )


                # --------------------------------------------------
                # TASKS
                # --------------------------------------------------

                existing_tasks = data.get(
                    "tasks"
                ) or []


                tasks = st.text_input(
                    "Tasks (comma separated)",
                    value=", ".join(existing_tasks),
                    key=f"tasks_{index}"
                )


                # --------------------------------------------------
                # LICENSE
                # --------------------------------------------------

                license_info = st.text_input(
                    "Licensing Information",
                    value=data.get(
                        "licensing_information"
                    ) or "",
                    key=f"license_{index}"
                )


                # --------------------------------------------------
                # SOURCE URL
                # --------------------------------------------------

                source_url = st.text_input(
                    "Dataset Source URL",
                    value=data.get(
                        "source_url"
                    ) or "",
                    key=f"source_url_{index}"
                )


                # --------------------------------------------------
                # DATASET DETAILS
                # --------------------------------------------------

                existing_details = data.get(
                    "dataset_details"
                ) or {}


                dataset_details = st.text_area(
                    "Dataset Details (JSON)",
                    value=json.dumps(
                        existing_details,
                        indent=4
                    ),
                    height=180,
                    key=f"details_{index}"
                )


                # --------------------------------------------------
                # VERIFICATION STATUS
                # --------------------------------------------------

                verification_status = st.selectbox(
                    "Verification Status",
                    [
                        "Needs Review",
                        "Verified",
                        "Rejected"
                    ],
                    key=f"verification_{index}"
                )


                # --------------------------------------------------
                # CREATE REVIEWED DATASET
                # --------------------------------------------------

                reviewed_dataset = {

                    "dataset_name": dataset_name,

                    "dataset_details": dataset_details,

                    "data_types": [
                        item.strip()
                        for item in data_types.split(",")
                        if item.strip()
                    ],

                    "modalities": [
                        item.strip()
                        for item in modalities.split(",")
                        if item.strip()
                    ],

                    "tasks": [
                        item.strip()
                        for item in tasks.split(",")
                        if item.strip()
                    ],

                    "licensing_information":
                        license_info
                        if license_info
                        else None,

                    "source_url":
                        source_url
                        if source_url
                        else None,

                    "verification_status":
                        verification_status
                }


                reviewed_datasets.append(
                    reviewed_dataset
                )


                st.divider()


            # --------------------------------------------------
            # SAVE REVIEWED DATASETS
            # --------------------------------------------------

            if st.button(
                "💾 Save Reviewed Datasets"
            ):

                # Store in session state
                st.session_state[
                    "reviewed_datasets"
                ] = reviewed_datasets


                # Save each dataset to SQLite
                for dataset in reviewed_datasets:

                    save_dataset(dataset)


                st.success(
                    "Dataset information saved successfully!"
                )


        # --------------------------------------------------
        # EXPORT SECTION
        # --------------------------------------------------

        if "reviewed_datasets" in st.session_state:

            st.subheader("📤 Export Dataset Information")


            export_data = st.session_state[
                "reviewed_datasets"
            ]


            # --------------------------------------------------
            # JSON EXPORT
            # --------------------------------------------------

            json_data = json.dumps(
                export_data,
                indent=4
            )


            st.download_button(
                label="📄 Download JSON",
                data=json_data,
                file_name="dataset_metadata.json",
                mime="application/json"
            )


            # --------------------------------------------------
            # CSV EXPORT
            # --------------------------------------------------

            csv_rows = []


            for item in export_data:

                row = {

                    "Dataset Name":
                        item["dataset_name"],

                    "Data Types":
                        ", ".join(
                            item["data_types"]
                        ),

                    "Modalities":
                        ", ".join(
                            item["modalities"]
                        ),

                    "Tasks":
                        ", ".join(
                            item["tasks"]
                        ),

                    "License":
                        item[
                            "licensing_information"
                        ],

                    "Source URL":
                        item[
                            "source_url"
                        ],

                    "Verification Status":
                        item[
                            "verification_status"
                        ]
                }


                csv_rows.append(row)


            df = pd.DataFrame(
                csv_rows
            )


            csv_data = df.to_csv(
                index=False
            )


            st.download_button(
                label="📊 Download CSV",
                data=csv_data,
                file_name="dataset_metadata.csv",
                mime="text/csv"
            )


    # --------------------------------------------------
    # ERROR HANDLING
    # --------------------------------------------------

    except ValueError as e:

        st.error(
            str(e)
        )


    except Exception as e:

        st.error(
            f"Unexpected error: {e}"
        )
