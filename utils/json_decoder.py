import json
from pathlib import Path
from typing import Optional

from models.section_data import SectionData
from utils import constants
from utils.enums.language import Language
from utils.enums.provider_type import ProviderType
from utils.enums.section_type import SectionType


class JsonDecoder:

    @staticmethod
    def decode(path_to_json_file: Path) -> list[SectionData]:
        with open(path_to_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        sections: list[SectionData] = []

        for section in data.get("sections", []):
            section_type = SectionType(section["type"])
            language = Language(section["language"])
            provider = ProviderType(section["provider"])

            tickers_raw = section["tickers"]

            if isinstance(tickers_raw, list):
                tickers = tickers_raw
            elif isinstance(tickers_raw, str):
                tickers = getattr(constants, tickers_raw)

            days_ahead: Optional[int] = section.get("days_ahead", None)
            days_behind: Optional[int] = section.get("days_behind", None)

            number_of_companies = section.get(
                "number_of_companies", section.get("number_of_articles")
            )

            sections.append(
                SectionData(
                    type=section_type,
                    language=language,
                    provider=provider,
                    tickers=tickers,
                    days_ahead=days_ahead,
                    days_behind=days_behind,
                    number_of_companies=number_of_companies,
                )
            )

        return sections
