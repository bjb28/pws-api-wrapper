"""Creates a session for use by the endpoints."""

# Standard Python Libraries
import os

# Third-Party Libraries
# Third Party Libraries
import requests


class APIKeyMissingError(Exception):
    """Exception for missing API Key Environment Variable."""

    pass


def get_api_key():
    """Get hte API Key from the os environment.

    Raises:
        APIKeyMissingError: Alerts on missing API Key.

    Returns:
        str: Returns the API Key as a string.
    """
    PENTEST_WS_API_KEY = os.environ.get("PENTEST_WS_API_KEY", None)
    if PENTEST_WS_API_KEY is None:
        raise APIKeyMissingError(
            "All methods require an API key. See "
            "https://pentest.ws/settings/api-key "
            "for how to retrieve an authentication token from "
            "pentest.ws"
        )
    return PENTEST_WS_API_KEY


session: requests.Session = requests.Session()
session.headers = requests.structures.CaseInsensitiveDict()
session.headers["X-API-KEY"] = get_api_key()
session.headers["accept"] = "application/json"
