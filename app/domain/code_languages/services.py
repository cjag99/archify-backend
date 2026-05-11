from uuid import UUID

from .models import CodeLanguagesModel
from .dtos import CodeLanguagesRequest
from .ports import CodeLanguagesPort

class CodeLanguagesService:
    def __init__(self, port: CodeLanguagesPort):
        self.port = port

    def create_code_language(self, data: CodeLanguagesRequest, token:str) -> CodeLanguagesModel:
        code_language = CodeLanguagesModel(
            name=data.name,
            file_extension=data.file_extension,
            icon=data.icon
        )
        self.port.save_code_language(code_language, token)
        return  code_language

    def get_all_code_languages(self, token: str) -> list[CodeLanguagesModel]:
        return self.port.get_all_code_languages(token)

    def get_code_language_by_id(self, code_language_id: UUID, token: str) -> CodeLanguagesModel | None:
        return self.port.get_code_language_by_id(code_language_id, token)

    def delete_code_language(self, code_language_id: UUID, token: str) -> None:
        return self.port.delete_code_language(code_language_id, token)

    def update_code_language(self, code_language_id: UUID, data: CodeLanguagesRequest, token: str) -> None:
        code_language = self.port.get_code_language_by_id(code_language_id, token)
        if code_language:
            if data.name and data.name != code_language.name:
                code_language.name = data.name

            if data.file_extension and data.file_extension != code_language.file_extension:
                code_language.file_extension = data.file_extension

            if data.icon and data.icon != code_language.icon:
                code_language.icon = data.icon

            self.port.save_code_language(code_language, token)