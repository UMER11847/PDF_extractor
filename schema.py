from typing import Optional, List
from pydantic import BaseModel


class DatasetMetadata(BaseModel):
    dataset_name: Optional[str] = None
    dataset_details: Optional[dict] = None
    data_types: Optional[List[str]] = None
    modalities: Optional[List[str]] = None
    tasks: Optional[List[str]] = None
    licensing_information: Optional[str] = None
    source_url: Optional[str] = None
