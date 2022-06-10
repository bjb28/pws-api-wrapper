#!/usr/bin/env pytest -vs
"""Tests for Scratchpad objects in pws-api-wrapper."""

# Third-Party Libraries
import pytest
from schema import SchemaError
import vcr

# Custom Libraries
from pws_api_wrapper import Scratchpad


class TestScratchpad:
    """Tests for the Scratchpad."""

    def test_init_validation_pass(self, scratchpad_dict):
        """Test the init validation."""

        scratchpad = Scratchpad(**scratchpad_dict)

        assert scratchpad.to_dict() == scratchpad_dict
