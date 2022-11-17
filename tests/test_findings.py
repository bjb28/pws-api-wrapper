#!/usr/bin/env pytest -vs
"""Tests for Finding objects in pws-api-wrapper."""

# Third-Party Libraries
import vcr

# Custom Libraries
from pws_api_wrapper import Finding


class TestFinding:
    """Tests for the Finding Endpoint."""

    @vcr.use_cassette("tests/vcr_cassettes/finding/create-200.yml")
    def test_create_200(self, finding_dict):
        """Test an API call to create a Finding."""
        # Delete id as teh API will not accept when creating.
        del finding_dict["id"]

        finding = Finding(**finding_dict)

        message = finding.create()

        # Add finding ID back to finding_dict
        finding_dict["id"] = finding.id

        assert isinstance(finding, Finding)
        assert finding.to_dict() == finding_dict
        assert message == "Finding Test Finding (nDa0BVxK) created."

    def test_init_validation_pass(self, finding_dict):
        """Test the init validation."""
        notePage = Finding(**finding_dict)

        assert notePage.to_dict() == finding_dict
