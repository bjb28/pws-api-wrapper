"""Host Object."""

from __future__ import annotations

# Standard Python Libraries
from ipaddress import ip_address
import json
import re
import sys
from typing import Any

# Third-Party Libraries
from requests import exceptions as requests_exceptions
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
                        OS_TYPES,
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

        try:
            self.host_path: str = f"{AbstractEndpoint.path}/hosts/{self.id}"
        except AttributeError:
            pass

        if self.eid:
            self.engagement_path: str = f"{AbstractEndpoint.path}/e/{self.eid}/hosts"

    def create(self) -> str:
        """Create an Host in pentest.ws."""
        self.pws_session.headers["Content-Type"] = "application/json"

        # Convert to dict to remove eid before json dump, API does not accept eid.
        host_dict: dict = self.to_dict()
        del host_dict["eid"]  # Drop eid as the API does not accept it.

        host_data: str = json.dumps(host_dict)

        # TODO Custom Exception (Issue 1)
        response: Response = self.pws_session.post(
            self.engagement_path, headers=self.pws_session.headers, data=host_data
        )

        # TODO Custom Exception (Issue 1)
        if response.status_code == 200:
            self.id = response.json()["id"]
            # FIXME The next line is flagged by mypy for Host not having an attribute "target".
            message: str = f"Host {self.target} ({self.id}) created."  # type: ignore
        elif response.status_code == 400:
            message = f"Error: {response.json()['msg']}"

        return message

    def delete(self) -> str:
        """Delete a host by id from pentest.ws API."""
        response: Response = self.pws_session.delete(f"{self.host_path}")

        # TODO Custom Exception (Issue 1)
        if response.status_code == 200:
            # FIXME The next line is flagged by mypy for Host not having an attribute "target".
            message: str = f"Host {self.target} ({self.id}) deleted."  # type: ignore
        elif response.status_code == 404:
            # FIXME The next line is flagged by mypy for Host not having an attribute "target".
            message = f"Error: Host {self.target} ({self.id}) not found"  # type: ignore

        return message

    @staticmethod
    def get(hid: str) -> Host:
        """Get a hosts from the API.."""
        # TODO Custom Exception (Issue 1)
        try:
            response: Response = Host.pws_session.get(
                f"{AbstractEndpoint.path}/hosts/{hid}"
            )
            response.raise_for_status()
        except requests_exceptions.HTTPError as err:
            raise SystemExit(err)
        else:
            return Host(**response.json())

    @staticmethod
    def get_all(eid: str) -> list[Host]:
        """Get all hosts from an Engagements."""
        # TODO Custom Exception (Issue 1)
        response: Response = Host.pws_session.get(
            f"{AbstractEndpoint.path}/e/{eid}/hosts"
        )
        hosts: list[Host] = list()

        for host_response in response.json():
            hosts.append(Host(**host_response))

        return hosts

    def update(self) -> str:
        """Update a Host."""
        self.pws_session.headers["Content-Type"] = "application/json"

        data = self.to_dict()
        # TODO Make these field meta data.
        del data["id"]
        del data["eid"]

        # TODO Custom Exception (Issue 1)
        response: Response = self.pws_session.put(
            f"{self.host_path}",
            headers=self.pws_session.headers,
            data=json.dumps(data),
        )

        # TODO Custom Exception (Issue 1)
        if response.status_code == 200:
            # FIXME The next line is flagged by mypy for Host not having an attribute "target".
            message: str = f"Host {self.target} ({self.id}) updated."  # type: ignore
        elif response.status_code == 400:
            message = f"Error: {response.json()['msg']}"

        return message
