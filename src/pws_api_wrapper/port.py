"""Port Object."""

from __future__ import annotations

# Standard Python Libraries
import json
import re
import sys
from typing import Any

# Third-Party Libraries
from requests import exceptions as requests_exceptions
from requests.models import Response
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
                Optional("checklist"): Or(
                    And(list, [dict, {str, str}]),
                    None,
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
                Optional("service"): Or(
                    str, None, error='"service" should be a string.'
                ),
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

        try:
            self.port_path: str = f"{AbstractEndpoint.path}/ports/{self.id}"
        except AttributeError:
            pass

        if self.hid:
            self.host_path: str = f"{AbstractEndpoint.path}/hosts/{self.hid}/ports"

    def create(self) -> str:  # pragma: no cover
        """Create an Port in pentest.ws.

        FIXME 500 Internal Server Error.
        The API will not return a 200 as non-400 errors
        return a 500 Internal Server Error. This function
        will have to be fixed/tested once word is received
        from Pentest.ws.

        Reminder to remove coverall exclude.

        """
        #
        self.pws_session.headers["Content-Type"] = "application/json"

        # Convert to dict to remove hid before json dump, API does not accept hid.
        port_dict: dict = self.to_dict()
        del port_dict["hid"]  # Drop hid as the API does not accept it.

        port_data: str = json.dumps(port_dict)

        # TODO Custom Exception (Issue 1)
        response: Response = self.pws_session.post(
            self.host_path, headers=self.pws_session.headers, data=port_data
        )

        # TODO Custom Exception (Issue 1)
        if response.status_code == 200:
            self.id = response.json()["id"]
            # FIXME The next line is flagged by mypy for Port not having an attribute "target".
            message: str = f"Port {self.port} ({self.id}) created."  # type: ignore
        elif response.status_code == 400:
            message = f"Error: {response.json()['msg']}"
        else:
            message = f"Error: {response.json()['msg']}"

        return message

    @staticmethod
    def get(pid: str) -> Port:
        """Get a port from the API.."""
        # TODO Custom Exception (Issue 1)
        try:
            response: Response = Port.pws_session.get(
                f"{AbstractEndpoint.path}/ports/{pid}"
            )
            response.raise_for_status()
        except requests_exceptions.HTTPError as err:
            raise SystemExit(err)
        else:
            return Port(**response.json())

    @staticmethod
    def get_all(hid: str) -> list[Port]:
        """Get all ports from a Host."""
        # TODO Custom Exception (Issue 1)
        response: Response = Port.pws_session.get(
            f"{AbstractEndpoint.path}/hosts/{hid}/ports"
        )
        ports: list[Port] = list()

        for host_response in response.json():
            ports.append(Port(**host_response))

        return ports
