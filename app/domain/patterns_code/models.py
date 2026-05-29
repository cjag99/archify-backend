from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.domain.jsonb_type import JsonDict

class PatternsCodeModel(BaseModel):
    pattern_id: UUID
    code_id: UUID
    code_snippet: JsonDict
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True, strict=False)
