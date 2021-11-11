"""Abstract Endpoint Object for Pentest.ws API."""

# Standard Python Libraries
from datetime import datetime
from typing import Any, Dict

# Custom Librares
from .session import session


class AbstractEndpoint(object):
    """Abstract class for all Pentest.ws API endpoints."""

    path: str = "https://pentest.ws/api/v1"
    pws_session = session

    class Meta:
        """Class Meta data."""

        abstract = True

    def to_dict(self) -> Dict[str, Any]:
        """Return object as dictionary."""
        dictionary: Dict[str, Any] = {}
        for attribute in self.__dict__.keys():
            if isinstance(getattr(self, attribute), datetime):
                time = datetime.strftime(
                    getattr(self, attribute), "%Y-%m-%dT%H:%M:%S.%f"
                )
                # Strip last three digits of microseconds and add the Z.
                time = f"{time[:-3]}Z"
                dictionary[attribute] = time
            elif (
                isinstance(getattr(self, attribute), str)
                and not attribute.startswith("__")
                and not attribute.endswith("path")
            ):
                dictionary[attribute] = getattr(self, attribute)
            elif (
                isinstance(getattr(self, attribute), bool)
                or isinstance(getattr(self, attribute), int)
                or isinstance(getattr(self, attribute), list)
            ):
                dictionary[attribute] = getattr(self, attribute)

        return dictionary
