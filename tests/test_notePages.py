#!/usr/bin/env pytest -vs
"""Tests for NotePage objects in pws-api-wrapper."""

# Third-Party Libraries
import pytest
from schema import SchemaError
import vcr

# Custom Libraries
from pws_api_wrapper import NotePage


class TestNotePage:
    """Tests for the NotePage."""

    @vcr.use_cassette("tests/vcr_cassettes/notePage/create-200.yml")
    def test_create_200(self, notePage_dict):
        """Test an API call to create a Note Page."""
        # Delete id as teh API will not accept when creating.
        del notePage_dict["id"]

        notePage = NotePage(**notePage_dict)

        message = notePage.create()

        # Add note page ID back to notePage_dict
        notePage_dict["id"] = notePage.id

        assert isinstance(notePage, NotePage)
        assert notePage.to_dict() == notePage_dict

    @vcr.use_cassette("tests/vcr_cassettes/notePage/create-400.yml")
    def test_create_400(self, notePage_dict):
        """Test an API call to fail at creating a Note Page."""
        # Add a fake engagement id to cause an error.
        notePage_dict["oid"] = "12345678"

        notePage = NotePage(**notePage_dict)

        message = notePage.create()

        assert isinstance(notePage, NotePage)
        assert message == "Error: Invalid engagements ID"

    def test_init_validation_pass(self, notePage_dict):
        """Test the init validation."""
        notePage = NotePage(**notePage_dict)

        assert notePage.to_dict() == notePage_dict

    @pytest.mark.parametrize(
        "attribute,value,error_message",
        [
            ("id", 4, '"id" should be 8 alphanumeric characters'),
            ("id", "asd123", '"id" should be 8 alphanumeric characters'),
            ("id", "abcd123!", '"id" should be 8 alphanumeric characters'),
            ("oid", 4, '"oid" should be 8 alphanumeric characters'),
            ("oid", "asd123", '"oid" should be 8 alphanumeric characters'),
            (
                "oid",
                "abcd123!",
                '"oid" should be 8 alphanumeric characters',
            ),
            ("title", "", 'Note Page "title" is required.'),
            ("content", 1, '"contented" should be a string or None.'),
            (
                "otype",
                "green",
                '"otype" should be one of the following:',
            ),
        ],
    )
    def test_init_validation_fail(self, attribute, value, error_message, notePage_dict):
        """Test the init validation fails when string value are not strings."""
        notePage_dict[attribute] = value
        with pytest.raises(SchemaError, match=error_message):
            NotePage(**notePage_dict)
