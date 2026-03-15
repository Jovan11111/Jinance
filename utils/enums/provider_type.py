from enum import Enum


class ProviderType(Enum):
    """Enumeration for choosing a type of provider to retrieve data.

    Types:
        YAHOO: Yahoo finance API.
    """

    YAHOO = "yahoo"
