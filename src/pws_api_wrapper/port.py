"""Port Object."""

from __future__ import annotations

# Standard Python Libraries
import re
import sys
from typing import Any

# Third-Party Libraries
from schema import And, Optional, Or, Regex, Schema, SchemaError

# Customer Libraries
from .abstract_endpoint import AbstractEndpoint

PROTOCOLS: list[str] = ["tcp", "udp"]
STATUSES: list[str] = ["Needs Review", "Vulnerable", "Checked", "Owned"]
STATES: list[str] = [
    "open",
    "filtered",
    "closed",
    "unfiltered",
    "open|filtered",
    "closed|filtered",
]


class Port(AbstractEndpoint):
    """Port Objects for Pentest.ws API.

    Attributes:
        checklist (list(dict(str, str))): List of dictionaries holding the port checklist.
        hid (str): The host id that the port belongs to.
        id (str): The port id from pentest.ws.
        notes (str): The host notes.
        port (int): The port
        proto (str): The ports protocol, tcp or udp.
        service (str): The service name for the port.
        status (str): The status of the port.
        state (str): The state of the port.
        version (str): The version of the service for the port.

    """

    def __init__(self, **kwargs):
        """Initialize port object."""
        schema: Schema = Schema(
            {
                Optional("checklist"): And(
                    list,
                    [dict, {str, str}],
                    error='"checklist" should be a list of dictionaries.',
                ),
                Optional("hid"): And(
                    str,
                    Regex(r"^[a-zA-Z0-9]{8,}$", flags=re.IGNORECASE),
                    error='"hid" should be 8 alphanumeric characters',
                ),
                Optional("id"): And(
                    str,
                    Regex(r"^[a-zA-Z0-9]{8,}$", flags=re.IGNORECASE),
                    error='"id" should be 8 alphanumeric characters',
                ),
                "port": And(
                    int,
                    lambda submitted_port: 0 <= submitted_port <= 65535,
                    error='"port" should be an intiger between 0 and 65,535.',
                ),
                Optional("proto"): Or(  # TODO Create a schema hook.
                    And(str, lambda submitted_proto: submitted_proto in PROTOCOLS),
                    And(None),
                    error='"proto" should be "tcp", "udp", or None',
                ),
                Optional("service"): And(str, error='"service" should be a string.'),
                Optional("status"): Or(  # TODO Create a schema hook.
                    And(str, lambda submitted_status: submitted_status in STATUSES),
                    And(None),
                    error='Not a valid "status".',
                ),
                Optional("state"): Or(  # TODO Create a schema hook.
                    And(str, lambda submitted_stat: submitted_stat in STATES),
                    And(None),
                    error='Not a valid "state".',
                ),
                Optional("notes"): Or(
                    And(str, error='"notes" should be a string'), None
                ),
                Optional("version"): Or(
                    And(str, error='"version" should be a string'), None
                ),
            }
        )

        try:
            validated_args: dict[str, Any] = schema.validate(kwargs)
        except SchemaError as err:
            # Raise error because 1 or more items were invald.
            print(err, file=sys.stderr)
            raise

        for key, value in validated_args.items():
            setattr(self, key, value)
