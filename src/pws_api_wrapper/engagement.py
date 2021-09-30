"""Engagement Object."""

from __future__ import annotations

# Standard Python Libraries
from datetime import datetime
import json
from typing import Any

# Third-Party Libraries
from requests.models import Response

from .abstract_endpoint import AbstractEndpoint


class Engagement(AbstractEndpoint):
    """Engagement Objects for Pentest.ws API.

    Attributes:
        archived (datetime): The date and time the engagement was archived in pentest.ws.
        client_id (str): The id for the client in pentest.ws.
        created_at (datetime): The date and time the engagement was created in pentest.ws.
        id (str): The edi from pentest.ws.
        name (str): The name of the engagement.
        notes (str): The notes about the engagement.

    Args:
        AbstractEndpoint ([type]): [description]

    """

    # TODO Create function to import xml to engagement

    path: str = f"{AbstractEndpoint.path}/e"

    def __init__(
        self,
        name: str,
        id: str = "",
        created_at: str = "",
        notes: str = "",
        client_id: str = "",
        archived: str = "",
    ):
        """Initialize engagement object.

        Args:
            id (str): The engagement ID.
            name (str): The name of the engagement.
            notes (str): The notes from the engagement.
            client_id (str): The id of the client associated with the engagement.
            created_at (str): The date and time the engagement was created, in UTC. Format: 'YYYY-MM-DDTHH:MM:SS.SSSZ'.
            archived (str): The date and time the engagement was archived, in UTC. Format: 'YYYY-MM-DDTHH:MM:SS.SSSZ'.
        """
        if id != "":
            self.id: str = id

        self.name: str = name
        self.notes: str = notes
        self.client_id: str = client_id

        if created_at != "" and created_at is not None:
            self.created_at: datetime = datetime.strptime(
                created_at.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S.%f%z"
            )

        if archived != "" and archived is not None:
            self.archived: datetime = datetime.strptime(
                archived.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S.%f%z"
            )

    def delete(self) -> str:
        """Delete an Engagement by name from pentest.ws API."""
        response: Response = Engagement.pws_session.delete(f"{self.path}/{self.id}")

        # TODO Custom Exception (Issue 1)
        if response.status_code == 200:
            message: str = f"Engagement {self.name} ({self.id}) deleted."
        elif response.status_code == 404:
            message = f"Error: Engagement {self.name} ({self.id}) not found"

        return message

    def create(self) -> str:
        """Create an Engagement in pentest.ws."""
        self.pws_session.headers["Content-Type"] = "application/json"

        response: Response = self.pws_session.post(
            self.path, headers=self.pws_session.headers, data=json.dumps(self.to_dict())
        )

        # TODO Custom Exception (Issue 1)
        if response.status_code == 200:
            self.id = response.json()["id"]
            message: str = f"Engagement {self.name} ({self.id}) created."
        elif response.status_code == 400:
            message = f"Error: {response.json()['msg']}"

        return message

    @staticmethod
    def get(name: str) -> Engagement:
        """Get an Engagement by name from pentest.ws API."""
        eid: str = Engagement.get_eid(name)
        # TODO Custom Exception (Issue 1)
        response: Response = Engagement.pws_session.get(f"{Engagement.path}/{eid}")

        return Engagement(**response.json())

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Get all Engagements."""
        # TODO Custom Exception (Issue 1)
        response: Response = Engagement.pws_session.get(Engagement.path)

        return response.json()

    @staticmethod
    def get_eid(name: str) -> str:
        """Get Engagement ID based on Name."""
        # TODO Handled multiple Engagements with the same name
        engagements: list[dict[str, Any]] = Engagement.get_all()

        # TODO Custom Exception (Issue 1)
        eid: str = list(
            filter(lambda engagement: engagement["name"] == name, engagements)
        )[0]["id"]

        return eid

    def update(self) -> str:
        """Update an Engagement."""
        self.pws_session.headers["Content-Type"] = "application/json"

        data = self.to_dict()
        # TODO Make these field meta data.
        del data["id"]
        del data["created_at"]
        del data["archived"]

        # TODO Custom Exception (Issue 1)
        response: Response = self.pws_session.put(
            f"{self.path}/{self.id}",
            headers=self.pws_session.headers,
            data=json.dumps(data),
        )

        # TODO Custom Exception (Issue 1)
        if response.status_code == 200:
            message: str = f"Engagement {self.name} ({self.id}) updated."
        elif response.status_code == 400:
            message = f"Error: {response.json()['msg']}"

        return message
