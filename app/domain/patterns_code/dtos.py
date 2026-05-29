from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.domain.jsonb_type import JsonDict

class PatternsCodeRequest(BaseModel):
    pattern_id: UUID
    code_id: UUID
    code_snippet: JsonDict

    model_config = ConfigDict(from_attributes=True, strict=False)
