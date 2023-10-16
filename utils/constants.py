from enum import Enum

BASE_URL = "https://www.kiwi.com/"

SEARCH_RESULTS_TIMEOUT = 60000


class StopsFilterValues(Enum):
    ONE_STOP = "Up to 1 stop"


class ExcludeCountriesFilterValues(Enum):
    UK = "United Kingdom"


PHONE_COUNTRY_CODE_VALUE_MATCH = {
    "+7": "ru"
}

NATIONALITY_CODE_VALUE_MATCH = {
    "Russia": "ru"
}

GENDER_CODE_VALUE_MATCH = {
    "Male": "mr"
}
