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

    @pytest.mark.parametrize(
        "attribute,value,error_message",
        [
            ("id", 4, '"id" should be 8 alphanumeric characters'),
            ("id", "asd123", '"id" should be 8 alphanumeric characters'),
            ("id", "abcd123!", '"id" should be 8 alphanumeric characters'),
            ("hid", 4, '"hid" should be 8 alphanumeric characters'),
            ("hid", "asd123", '"hid" should be 8 alphanumeric characters'),
            ("hid", "abcd123!", '"hid" should be 8 alphanumeric characters'),
            ("title", "", 'Scratchpad "title" is required.'),
            ("language", "green", 'language" should be None or one of the following:'),
            ("id", 4, '"id" should be 8 alphanumeric characters'),
            ("id", "asd123", '"id" should be 8 alphanumeric characters'),
            ("id", "abcd123!", '"id" should be 8 alphanumeric characters'),
            ("content", 1, '"contented" should be a string or None.'),
            ("type", "green", '"type" should be None or one of the following:'),
            ("type", 1, '"type" should be None or one of the following:'),
        ],
    )
    def test_init_validation_fail(
        self, attribute, value, error_message, scratchpad_dict
    ):
        """Test the init validation fails when string value are not strings."""
        scratchpad_dict[attribute] = value
        with pytest.raises(SchemaError, match=error_message):
            Scratchpad(**scratchpad_dict)
