#!/usr/bin/env pytest -vs
"""Tests for Finding objects in pws-api-wrapper."""

# Third-Party Libraries
import vcr

# Custom Libraries
from pws_api_wrapper import Finding


class TestFinding:
    """Tests for the Finding Endpoint."""

        """Test the init validation."""
        notePage = Finding(**finding_dict)

        assert notePage.to_dict() == finding_dict
