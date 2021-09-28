"""Host Object."""

# Standard Python Libraries
from ipaddress import ip_address
import re
import sys
from typing import Any, Dict

# Third-Party Libraries
from schema import And, Schema, SchemaError, Optional, Regex, Use

# Customer Libraries
from .abstract_endpoint import AbstractEndpoint


class Host(AbstractEndpoint):
    """Host Objects for Pentest.ws API.

    Attributes:
        board_id (str): The board id for the host.
        flagged (bool): Indicates if the host is flagged.
        hostnames (str): The hostnames assigned to the host.
        id (str): The host id from pentest.ws.
        label (str): The label assigned to the host.
        notes (str): The host notes.
        os (str): The specific operating system of the host.
        os_type (str): The operating system of the host.
        out_of_scope (bool): Indicates if the host is out of scope.
        reviewed (bool): Indicates if the host has been reviewed.
        shell (bool): Indicates there is a shell on the host.
        target (str): The ip address of the host.
        thumbs_down (bool): Indicates if the host has a thumbs down.
        thumbs_up (bool): Indicates if the host has a thumbs up.
        type (str): The type of assigned to the host.

    """

    def __init__(self, **kwargs):
        """Initialize host object."""
        schema: Schema = Schema(
            {
                Optional("board_id"): And(
                    str,
                    Regex(r"^[a-zA-Z0-9]{8,}$", flags=re.IGNORECASE),
                    error='"board_id" should be 8 alphanumeric characters',
                ),
                Optional("flagged"): And(
                    bool, error='"flagged" should be True/False boolean'
                ),
                Optional("hostnames"): And(str, error='"hostnames" should be a string'),
                Optional("id"): And(
                    str,
                    Regex(r"^[a-zA-Z0-9]{8,}$", flags=re.IGNORECASE),
                    error='"id" should be 8 alphanumeric characters',
                ),
                Optional("label"): And(str, error='"label" should be a string.'),
                Optional("notes"): And(str, error='"notes" should be a string'),
                Optional("os"): And(str, error='"os" should be a string'),
                Optional("os_type"): And(str, error='"os_type" should be a string'),
                Optional("out_of_scope"): And(
                    bool, error='"out_of_scope" should be True/False boolean'
                ),
                Optional("reviewed"): And(
                    bool, error='"reviewed" should be True/False boolean'
                ),
                Optional("shell"): And(
                    bool, error='"shell" should be True/False boolean'
                ),
                "target": And(
                    str,
                    Use(lambda ip: str(ip_address(ip))),
                    error="Target should be a valid IPv4 Address",
                ),
                Optional("thumbs_down"): And(
                    bool, error='"thumbs_down" should be True/False boolean'
                ),
                Optional("thumbs_up"): And(
                    bool, error='"thumbs_up" should be True/False boolean'
                ),
                Optional("type"): And(str, error='"type" should be a string'),
            }
        )

        try:
            validated_args: Dict[str, Any] = schema.validate(kwargs)
        except SchemaError as err:
            # Raise error because 1 or more items were invald.
            print(err, file=sys.stderr)
            raise

        for key, value in validated_args.items():
            setattr(self, key, value)
        self.path: str = f"{AbstractEndpoint.path}/hosts/{id}"
