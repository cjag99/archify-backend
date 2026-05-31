from uuid import UUID

from .models import PatternsCodeModel
from .dtos import PatternsCodeRequest
from .ports import PatternsCodePort


class PatternCodeService:
    def __init__(self, port: PatternsCodePort):
        self.port = port

    def create_pattern_code(self, data: PatternsCodeRequest, token: str) -> PatternsCodeModel | None:
        pattern_code = PatternsCodeModel(
            pattern_id=data.pattern_id,
            code_id=data.code_id,
            code_snippet=data.code_snippet
        )
        self.port.save_pattern_code(pattern_code, token)
        return  pattern_code

    def get_all_pattern_codes(self) -> list[PatternsCodeModel] | None:
        return  self.port.get_all_pattern_codes()

    def get_pattern_code_by_id(self, code_id: UUID, pattern_id: UUID) -> list[PatternsCodeModel] | None:
        return self.port.get_pattern_code_by_id(pattern_id)

    def get_pattern_code_by_all_id(self, code_id: UUID, pattern_id: UUID) -> PatternsCodeModel:
        return self.port.get_pattern_code_by_all_id(code_id, pattern_id)
    def delete_pattern_code(self, code_id: UUID, pattern_id: UUID, token: str) -> None:
        self.port.delete_pattern_code(code_id, pattern_id, token)

    def update_pattern_code(self, code_id: UUID, pattern_id: UUID, data: PatternsCodeRequest, token: str) -> PatternsCodeModel:
        pattern_code = self.port.get_pattern_code_by_id(code_id, pattern_id)
        pattern_code.code_snippet = data.code_snippet
        self.port.save_pattern_code(pattern_code, token)
        return  pattern_code
