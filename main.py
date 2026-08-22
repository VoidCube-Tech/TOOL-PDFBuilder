from json import load
from pathlib import Path
import sys

from data import Data
from generate_pdf import generate_pdf


ROOT_DIR = Path(__file__).resolve().parent


JSON_DIR = ROOT_DIR / "pdf"


def _require_string(payload: dict, key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Campo obrigatório inválido: {key}")
    return value


def _optional_string(payload: dict, key: str) -> str:
    value = payload.get(key, "")
    if value is None:
        return ""
    if not isinstance(value, str):
        raise TypeError(f"Campo inválido: {key} precisa ser uma string")
    return value


def _validate_string_list(payload: dict, key: str) -> list[str]:
    value = payload.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise TypeError(f"Campo inválido: {key} precisa ser uma lista")
    if not all(isinstance(item, str) for item in value):
        raise TypeError(f"Campo inválido: {key} precisa conter apenas strings")
    return value


def _validate_object_list(payload: dict, key: str, required_fields: tuple[str, ...]) -> list[dict]:
    value = payload.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise TypeError(f"Campo inválido: {key} precisa ser uma lista")

    validated = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            raise TypeError(f"Campo inválido: {key}[{index}] precisa ser um objeto")
        for field in required_fields:
            if field not in item or not isinstance(item[field], (str, int)):
                raise ValueError(f"Campo inválido: {key}[{index}].{field}")
        validated.append(item)

    return validated


def _validate_no_benefits(payload: dict) -> list:
    value = payload.get("no_benefits", [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise TypeError("Campo inválido: no_benefits precisa ser uma lista")

    validated = []
    for index, item in enumerate(value, start=1):
        if isinstance(item, str):
            validated.append(item)
            continue
        if not isinstance(item, dict):
            raise TypeError(f"Campo inválido: no_benefits[{index}] precisa ser string ou objeto")
        for field in ("title", "description", "effort", "impact"):
            if field not in item or not isinstance(item[field], str):
                raise ValueError(f"Campo inválido: no_benefits[{index}].{field}")
        validated.append(item)

    return validated


def load_json_payload(json_path: Path) -> dict:
    if not json_path.exists():
        available = sorted(path.name for path in JSON_DIR.glob("*.json"))
        suffix = f" Arquivos disponíveis: {', '.join(available)}" if available else ""
        raise FileNotFoundError(f"JSON não encontrado: {json_path.name}.{suffix}")

    with json_path.open("r", encoding="utf-8") as file:
        payload = load(file)

    if not isinstance(payload, dict):
        raise ValueError("O JSON raiz precisa ser um objeto")

    return payload


def build_data_from_json(json_path: Path) -> Data:
    payload = load_json_payload(json_path)

    return Data(
        name=_require_string(payload, "name"),
        audit_description=_optional_string(payload, "audit_description"),
        audit_categories=_validate_object_list(payload, "audit_categories", ("name", "score", "description")),
        finding_category=_optional_string(payload, "finding_category"),
        finding_title=_optional_string(payload, "finding_title"),
        finding_description=_optional_string(payload, "finding_description"),
        finding_impact=_optional_string(payload, "finding_impact"),
        strengths=_validate_string_list(payload, "strengths"),
        attention_points=_validate_string_list(payload, "attention_points"),
        insight_kicker=_optional_string(payload, "insight_kicker") or "INSIGHT",
        insight_title=_optional_string(payload, "insight_title"),
        insight_intro=_optional_string(payload, "insight_intro"),
        trend_data=_validate_object_list(payload, "trend_data", ("label", "value")),
        insight_stat1_label=_optional_string(payload, "insight_stat1_label"),
        insight_stat1_value=_optional_string(payload, "insight_stat1_value"),
        insight_stat2_label=_optional_string(payload, "insight_stat2_label"),
        insight_stat2_value=_optional_string(payload, "insight_stat2_value"),
        interpretation=_optional_string(payload, "interpretation"),
        now_steps=_validate_object_list(payload, "now_steps", ("title", "description", "effort", "impact")),
        next_steps=_validate_object_list(payload, "next_steps", ("title", "description", "effort", "impact")),
        future_steps=_validate_object_list(payload, "future_steps", ("title", "description", "effort", "impact")),
        no_benefits=_validate_no_benefits(payload),
    )


def resolve_json_path() -> list[Path]:
    if len(sys.argv) > 1:
        candidate = Path(sys.argv[1])
        return [candidate if candidate.is_absolute() else JSON_DIR / candidate]

    json_files = sorted(JSON_DIR.glob("*.json"))
    if len(json_files) == 1:
        return json_files
    if not json_files:
        raise FileNotFoundError("Nenhum arquivo JSON encontrado na pasta 'pdf'")
    raise ValueError("Passe o nome do JSON no comando. Exemplo: python main.py ola.json")


if __name__ == "__main__":
    json_paths = resolve_json_path()
    for i, json_path in enumerate(json_paths):
        data = build_data_from_json(json_path)
        generate_pdf(data, output_filename=str(json_path.with_suffix(".pdf")))
        print(f"PDF gerado com sucesso [{i + 1}]: {json_path.with_suffix('.pdf')}")