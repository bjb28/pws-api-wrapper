"""Host Object."""

from __future__ import annotations

# Standard Python Libraries
from ipaddress import ip_address
import re
import sys
from typing import Any

# Third-Party Libraries
from requests.models import Response
from schema import And, Optional, Or, Regex, Schema, SchemaError, Use

# Customer Libraries
from .abstract_endpoint import AbstractEndpoint

OS_TYPES: list[tuple[str, str]] = [
    ("Android", "Android"),
    ("Apple", "Apple"),
    ("Linux", "Linux"),
    ("question", "Unknown"),
    ("Windows", "Windows"),
]
TYPES: list[tuple[str, str]] = [
    ("wifi", "Access Point"),
    ("volume-up", "Audio"),
    ("laptop", "Laptop"),
    ("mobile", "Mobile"),
    ("phone", "Phone"),
    ("printer", "Printer"),
    ("question", "Unknown"),
    ("sitemap", "Router"),
    ("server", "Server"),
    ("tablet", "Tablet"),
    ("tv", "TV"),
    ("desktop", "Workstation"),
]


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
                Optional("eid"): And(
                    str,
                    Regex(r"^[a-zA-Z0-9]{8,}$", flags=re.IGNORECASE),
                    error='"eid" should be 8 alphanumeric characters',
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
                Optional("label"): Or(
                    And(str, error='"label" should be a string.'), None
                ),
                Optional("notes"): Or(
                    And(str, error='"notes" should be a string'), None
                ),
                Optional("os"): Or(And(str, error='"os" should be a string'), None),
                Optional("os_type"): And(
                    str,
                    Or(
                        lambda submitted_os_type: submitted_os_type
                        in [os_type[0] for os_type in OS_TYPES],
                        lambda submitted_os_type: submitted_os_type
                        in [os_type[1] for os_type in OS_TYPES],
                        TYPES,
                    ),  # TODO Create a schema hook.
                    error='Not a valid "os_type".',
                ),
                Optional("out_of_scope"): And(
                    bool, error='"out_of_scope" should be True/False boolean'
                ),
                Optional("owned"): And(
                    bool, error='"owned" should be True/False boolean'
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
                Optional("type"): And(
                    str,
                    Or(
                        lambda submitted_type: submitted_type
                        in [type[0] for type in TYPES],
                        lambda submitted_type: submitted_type
                        in [type[1] for type in TYPES],
                        TYPES,
                    ),  # TODO Create a schema hook.
                    error='Not a valid "type".',
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
        self.path: str = f"{AbstractEndpoint.path}/hosts/{id}"

    @staticmethod
    def get_all(eid: str) -> list[Host]:
        """Get all hosts from an Engagements."""
        response: Response = Host.pws_session.get(
            f"{AbstractEndpoint.path}/e/{eid}/hosts"
        )
        hosts: list[Host] = list()

        for host_response in response.json():
            hosts.append(Host(**host_response))

        return hosts
