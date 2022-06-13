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

    @vcr.use_cassette("tests/vcr_cassettes/scratchpad-create-200.yml")
    def test_create_200(self, scratchpad_dict):
        """Test an API call to create an Scratchpad."""
        scratchpad = Scratchpad(**scratchpad_dict)

        message = scratchpad.create()

        # Add host ID back to host_dict
        scratchpad_dict["id"] = scratchpad.id

        assert isinstance(scratchpad, Scratchpad)
        assert scratchpad.to_dict() == scratchpad_dict
        assert message == "Scratchpad README.md (1abWR16y) created."

    @vcr.use_cassette("tests/vcr_cassettes/scratchpad-create-400.yml")
    def test_create_400(self, scratchpad_dict):
        """Test an API call to create an Scratchpad with an type."""
        # Add fake host id to cause error.
        scratchpad_dict["hid"] = "12345678"

        scratchpad = Scratchpad(**scratchpad_dict)

        message = scratchpad.create()

        assert isinstance(scratchpad, Scratchpad)
        assert message == "Error: Invalid Host ID"

    @vcr.use_cassette("tests/vcr_cassettes/scratchpad-get-200.yml")
    def test_get_200(self, scratchpad_dict):
        """Test an API call to get a scratchpad."""
        scratchpad = Scratchpad.get("1abWR16y")

        assert isinstance(scratchpad, Scratchpad)
        assert scratchpad.to_dict() == scratchpad_dict

    @vcr.use_cassette("tests/vcr_cassettes/scratchpad-get-400.yml")
    def test_get_400(self):
        """Test an API call to get a scratchpad that returns an error."""
        with pytest.raises(SystemExit):
            Scratchpad.get("abcd1234")

    @vcr.use_cassette("tests/vcr_cassettes/scratchpad-get-all-200.yml")
    def test_get_call(self):
        """Test an API call to get all scratchpads for a Host."""
        scratchpads = Scratchpad.get_all("za4AlEP6")

        assert len(scratchpads) == 3

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
