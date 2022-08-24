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
            ("object_id", 4, '"object_id" should be 8 alphanumeric characters'),
            ("object_id", "asd123", '"object_id" should be 8 alphanumeric characters'),
            (
                "object_id",
                "abcd123!",
                '"object_id" should be 8 alphanumeric characters',
            ),
            ("title", "", 'Note Page "title" is required.'),
            ("content", 1, '"contented" should be a string or None.'),
            (
                "object_type",
                "green",
                '"object_type" should be one of the following:',
            ),
        ],
    )
    def test_init_validation_fail(self, attribute, value, error_message, notePage_dict):
        """Test the init validation fails when string value are not strings."""
        notePage_dict[attribute] = value
        with pytest.raises(SchemaError, match=error_message):
            NotePage(**notePage_dict)
