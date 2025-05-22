from pydantic import BaseModel
from typing import List, Optional

class ClassificationRequest(BaseModel):
    text: str
    config_name: Optional[str] = None

class ClassificationResponse(BaseModel):
    classification: str
    confidence: Optional[float] = None
    model: str
    config_used: str
    available_classes: List[str]