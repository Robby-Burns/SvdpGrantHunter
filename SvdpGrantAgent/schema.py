from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class GrantStatus(str, Enum):
    SCOUTED = "Scouted"
    DRAFTING = "Drafting"
    PENDING_REVIEW = "Pending_Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class GrantRecord(BaseModel):
    grant_id: str
    grant_source_url: str
    extracted_requirements: List[str] = Field(default_factory=list)
    draft_payload: dict = Field(default_factory=dict)
    human_feedback: Optional[str] = None
    status: GrantStatus = GrantStatus.SCOUTED

class OrganzationFact(BaseModel):
    category: str  # e.g., "Finance", "Mission", "Impact"
    content: str
    source_document: str
    citation_trace: str
