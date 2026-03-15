from enum import Enum


class Language(Enum):
    """Enumeration used for choosing a language a part of the report should be in.

    Types:
        SERBIAN: Report is generated in Serbian.
        ENGLISH: Report is generated in English.
    """

    SERBIAN = "sr"
    ENGLISH = "en"
