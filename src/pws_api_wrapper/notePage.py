"""NotePage Object."""

# Standard Python Libraries
import re
import sys
from typing import Any

# Third-Party Libraries

# Customer Libraries
from .abstract_endpoint import AbstractEndpoint

OBJECT_TYPES: list[str] = ["e", "hosts", "ports"]


class NotePage(AbstractEndpoint):
    """NotePage Objects fro Pentest.ws API.

    Attributes:
            content (str): The content of the Note Page.
            id (str): The Note Page id from pentest.ws.
            object_type (str): The object type the Note Page is under.
            object_id (str): The object id that the Note Page falls under.
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
                Optional("object_id"): And(
                    str,
                    Regex(r"^[a-zA-Z0-9]{8,}$", flags=re.IGNORECASE),
                    error='"object_id" should be 8 alphanumeric characters',
                ),
                Optional("object_type"): And(
                    str,
                    Or(
                        lambda submitted_object_type: submitted_object_type
                        in [object_type[0] for object_type in OBJECT_TYPES],
                        lambda submitted_os_type: submitted_os_type
                        in [object_type[1] for object_type in OBJECT_TYPES],
                        OBJECT_TYPES,
                    ),  # TODO Create a schema hook.
                    error=f'"object_type" should be one of the following: {str(OBJECT_TYPES)[1:-1]}',
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
