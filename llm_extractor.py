import os
import json

from dotenv import load_dotenv
from google import genai

from schema import DatasetMetadata


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")


client = genai.Client(api_key=api_key)


def extract_dataset_metadata(text):

    prompt = f"""
You are a research data extraction assistant.

Analyze the following research paper text and identify ALL datasets
used, mentioned, or introduced in the paper.

For each dataset, extract only information explicitly supported
by the paper.

Do not invent information.

If information is not mentioned, return null.

Return ONLY a JSON array.

Each item in the array must follow this structure:

[
    {{
        "dataset_name": "string",
        "dataset_details": {{
            "total_images": null,
            "training_images": null,
            "testing_images": null,
            "other_details": null
        }},
        "data_types": [],
        "modalities": [],
        "tasks": [],
        "licensing_information": null,
        "source_url": null
    }}
]

Paper text:

{text}
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        generation_config={
            "thinking_level": "low"
        }
    )

    result = interaction.output_text.strip()

    print("Gemini raw response:")
    print(repr(result))

    if result.startswith("```"):
        result = result.replace("```json", "", 1)
        result = result.replace("```", "")
        result = result.strip()

    try:

        data = json.loads(result)

        if not isinstance(data, list):
            data = [data]

        metadata = [
            DatasetMetadata.model_validate(item)
            for item in data
        ]

        return metadata

    except json.JSONDecodeError:
        raise ValueError(
            "Gemini did not return valid JSON."
        )

    except Exception as e:
        raise ValueError(
            f"Could not validate Gemini response: {e}"
        )
