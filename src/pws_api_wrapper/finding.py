"""Finding Object."""

from __future__ import annotations

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


class Finding(AbstractEndpoint):
    """Finding Objects for Pentest.ws API

    Attributes:
        id (str): The finding id from pentest.ws.
        eid (str): The engagement id that the finding belongs to.
        finding_id (str): The id assigned to the finding for the report.
        title (str): The title for the finding.
        environment (str): The finding's environment.
        category (str): The finding's category.
        risk_level (str): THe finding's risk level
        cvss2_num (float): The finding's CVSS v2 score.
        cvss2_str (str): The finding's CVSS v2 vector.
        cvss3_num (float): The finding's CVSS v3 score.
        cvss3_str (str): The finding's CVSS v3 vector.
        dread (list): A list of strings that represent the Dread score.
        background (str): The background text for the finding.
        desc_brief (str): The a brief description of the finding.
        desc_full (str): The a full description of the finding.
        impact_brief (str): The a brief impact of the finding.
        impact_full (str): The a full impact of the finding.
        reco_brief (str): The a brief recommendation for the finding.
        reco_full (str): The a full recommendation for the finding.
        reco_effort (str): Unknown
        targets (str): Targets from the engagement associated with the finding.
        references (str): Reference information associated with the finding.
        evidence (str): Evidence to support the finding.
        validation_steps (str): Steps to validate the finding.
        remediation_log (str): A log of remediation steps taken.
        created_at (str): Timestamp the finding was created in YYYY-MM-DDTHH:MM:SS.mmmZ.

    """

    def __init__(self, **kwargs):
        """Initialize finding object."""
        schema: Schema = Schema(
            {
                Optional("id"): And(
                    str,
                    Regex(r"^[a-zA-Z0-9]{8,}$", flags=re.IGNORECASE),
                    error='"id" should be 8 alphanumeric characters',
                ),
                Optional("eid"): And(
                    str,
                    Regex(r"^[a-zA-Z0-9]{8,}$", flags=re.IGNORECASE),
                    error='"e" should be 8 alphanumeric characters',
                ),
                Optional("finding_id"): Or(
                    And(str, error='"finding_id" should be a string'), None
                ),
                "title": And(
                    str,
                    Regex(r"[a-zA-Z0-9]+", flags=re.IGNORECASE),
                    error='Finding "title" is required.',
                ),
                Optional("environment"): Or(
                    And(str, error='"environment" should be a string'), None
                ),
                Optional("category"): Or(
                    And(str, error='"category" should be a string'), None
                ),
                Optional("risk_level"): Or(
                    And(str, error='"risk_level" should be a string'), None
                ),
                Optional("cvss2_num"): Or(
                    And(float, error='"cvss2_num" should be a string'), None
                ),
                Optional("cvss2_str"): Or(
                    And(str, error='"cvss2_str" should be a string'), None
                ),
                Optional("cvss3_num"): Or(
                    And(float, error='"cvss3_num" should be a string'), None
                ),
                Optional("cvss3_str"): Or(
                    And(str, error='"cvss3_str" should be a string'), None
                ),
                Optional("dread"): Or(
                    # TODO Improve dread checks.
                    And(list, [str]),
                    None,
                    error='"dread" should be a list of strings.',
                ),
                Optional("background"): Or(
                    And(str, error='"background" should be a string'), None
                ),
                Optional("desc_brief"): Or(
                    And(str, error='"desc_brief" should be a string'), None
                ),
                Optional("desc_full"): Or(
                    And(str, error='"desc_full" should be a string'), None
                ),
                Optional("impact_brief"): Or(
                    And(str, error='"impact_brief" should be a string'), None
                ),
                Optional("impact_full"): Or(
                    And(str, error='"impact_full" should be a string'), None
                ),
                Optional("reco_brief"): Or(
                    And(str, error='"reco_brief" should be a string'), None
                ),
                Optional("reco_full"): Or(
                    And(str, error='"reco_full" should be a string'), None
                ),
                Optional("reco_effort"): Or(
                    And(str, error='"reco_effort" should be a string'), None
                ),
                Optional("targets"): Or(
                    And(str, error='"targets" should be a string'), None
                ),
                Optional("references"): Or(
                    And(str, error='"references" should be a string'), None
                ),
                Optional("evidence"): Or(
                    And(str, error='"evidence" should be a string'), None
                ),
                Optional("validation_steps"): Or(
                    And(str, error='"validation_steps" should be a string'), None
                ),
                Optional("remediation_log"): Or(
                    And(str, error='"remediation_log" should be a string'), None
                ),
                Optional("created_at"): Or(
                    # TODO Improve date time checks.
                    And(str, error='"created_at" should be a string'),
                    None,
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
            # If a Findings ID is provided creates the finding_path.
            self.finding_path: str = f"{AbstractEndpoint.path}/findings/{self.id}"
        except AttributeError:
            pass

        if self.eid:
            # Creates and engagement_path if eid is provided.
            self.engagement_path: str = f"{AbstractEndpoint.path}/e/{self.eid}/findings"

    def create(self) -> str:
        """Create a Finding in pentest.ws."""
        self.pws_session.headers["Content-Type"] = "application/json"

        finding_dict: dict = self.to_dict()
        del finding_dict["eid"]  # Drop eid as the API does not accept it.

        finding_data: str = json.dumps(finding_dict)

        # TODO Custom Exception (Issue 1)
        response: Response = self.pws_session.post(
            self.engagement_path, headers=self.pws_session.headers, data=finding_data
        )

        # TODO Custom Exception (Issue 1)
        if response.status_code == 200:
            self.id = response.json()["id"]
            # FIXME The next line is flagged by mypy for NotePage not having an attribute "title".
            message: str = f"Finding {self.title} ({self.id}) created."  # type: ignore
        elif response.status_code == 400:
            message = f"Error: {response.json()['msg']}"

        return message
