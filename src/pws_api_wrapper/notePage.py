"""NotePage Object."""

# Standard Python Libraries
import json
import re
import sys
from typing import Any

# Third-Party Libraries
from requests.models import Response
from schema import And, Optional, Or, Regex, Schema, SchemaError

# Customer Libraries
from .abstract_endpoint import AbstractEndpoint

OBJECT_TYPES: list[str] = ["e", "hosts", "ports"]


class NotePage(AbstractEndpoint):
    """NotePage Objects fro Pentest.ws API.

    Attributes:
            content (str): The content of the Note Page.
            id (str): The Note Page id from pentest.ws.
            otype (str): The object type the Note Page is under.
            oid (str): The object id that the Note Page falls under.
            title (str): The Note Page title.

    """

    def __init__(self, **kwargs):
        """Initialize note page object."""
        schema: Schema = Schema(
            {
                Optional("content"): Or(
                    str, None, error='"contented" should be a string or None.'
                ),
                Optional("id"): And(
                    str,
                    Regex(r"^[a-zA-Z0-9]{8,}$", flags=re.IGNORECASE),
                    error='"id" should be 8 alphanumeric characters',
                ),
                # TODO Make oid and otype both required when one is present.
                Optional("oid"): And(
                    str,
                    Regex(r"^[a-zA-Z0-9]{8,}$", flags=re.IGNORECASE),
                    error='"oid" should be 8 alphanumeric characters',
                ),
                Optional("otype"): And(
                    str,
                    Or(
                        lambda submitted_otype: submitted_otype
                        in [otype[0] for otype in OBJECT_TYPES],
                        lambda submitted_os_type: submitted_os_type
                        in [otype[1] for otype in OBJECT_TYPES],
                        OBJECT_TYPES,
                    ),  # TODO Create a schema hook.
                    error=f'"otype" should be one of the following: {str(OBJECT_TYPES)[1:-1]}',
                ),
                "title": And(
                    str,
                    Regex(r"[a-zA-Z0-9]+", flags=re.IGNORECASE),
                    error='Note Page "title" is required.',
                ),
            }
        )

        try:
            validated_args: dict[str, Any] = schema.validate(kwargs)
        except SchemaError as err:
            # Raise error because 1 or more items were invalid.
            print(err, file=sys.stderr)
            raise

        for key, value in validated_args.items():
            setattr(self, key, value)

        try:
            # If a notePad ID, oid, and otype is provided, creates the notePad_path.
            self.notepad_path: str = (
                f"{AbstractEndpoint.path}/{self.otype}/{self.oid}/notepages/{self.id}"
            )
        except AttributeError:
            pass

        if self.oid and self.otype:
            # Creates and object_path if oid and otype are provided.
            self.object_path: str = (
                f"{AbstractEndpoint.path}/{self.otype}/{self.oid}/notepages"
            )

    def create(self) -> str:
        """Create a Note Pad in pentest.ws."""
        self.pws_session.headers["Content-Type"] = "application/json"

        notepad_dict: dict = self.to_dict()

        notepad_data: str = json.dumps(notepad_dict)

        # TODO Custom Exception (Issue 1)
        response: Response = self.pws_session.post(
            self.object_path, headers=self.pws_session.headers, data=notepad_data
        )

        # TODO Custom Exception (Issue 1)
        if response.status_code == 200:
            self.id = response.json()["id"]
            # FIXME The next line is flagged by mypy for NotePage not having an attribute "title".
            message: str = f"Note Page {self.title} ({self.id}) created."  # type: ignore
        elif response.status_code == 400:
            message = f"Error: {response.json()['msg']}"

        return message
