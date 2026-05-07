from uuid import UUID

from .client import supabase_client
from ...domain.patterns.models import PatternModel
from ...domain.patterns.ports import PatternPort


class SupabasePatternRepository(PatternPort):
    def __init__(self):
        self.client = supabase_client
        self.table_name = "patterns"

    def save_pattern(self, pattern: PatternModel) -> None:
        try:
            pattern_dict = {
                "name": pattern.name,
                "description": pattern.description,
                "base_structure": pattern.base_structure
            }
            self.client.from_(self.table_name).upsert(pattern_dict).execute()
        except Exception as e:
            print(f"Erro al guardar: {e}")

    def get_pattern_by_id(self, pattern_id: UUID) -> PatternModel | None:
        try:
            res = self.client.from_(self.table_name).select("*").eq("id", str(pattern_id)).execute()
            if not getattr(res, "data", None):
                return None

            return PatternModel(**res.data[0])
        except Exception as e:
            print(f"Error al obtener: {e}")
            return None

    def get_all_patterns(self) -> list[PatternModel] | None:
        try:
            res = self.client.from_(self.table_name).select("*").execute()
            if not getattr(res, "data", None):
                return None

            return [PatternModel(**row) for row in res.data]
        except Exception as e:
            print(f"Error al obtener todos los patterns: {e}")
            return None

    def delete_pattern(self, pattern_id: UUID) -> None:
        try:
            self.client.from_(self.table_name).delete().eq("id", pattern_id).execute()
        except Exception as e:
            print(f"Error al eliminar pattern: {e}")
