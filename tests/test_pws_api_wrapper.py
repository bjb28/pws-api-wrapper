#!/usr/bin/env pytest -vs
"""Tests for pws-api-wrapper."""

# Standard Python Libraries
from datetime import datetime

# Third-Party Libraries
import pytest
import vcr

# Custom Libraries
from pws_api_wrapper import AbstractEndpoint, APIKeyMissingError, Engagement
from pws_api_wrapper.session import get_api_key


class TestPWSession:
    """Tests the PWSession."""

    def test_api_key_exception(self, monkeypatch):
        """Test that api key of none rases exception."""
        monkeypatch.delenv("PENTEST_WS_API_KEY")
        with pytest.raises(APIKeyMissingError):
            get_api_key()


class TestAbstractEndpoint:
    """Tests for the Abstract Endpoint."""

    def test_path(self):
        """Test the path is correctly returned."""
        assert isinstance(AbstractEndpoint.path, str)
        assert (
            AbstractEndpoint.path == "https://pentest.ws/api/v1"
        ), "The url should be 'https://pentest.ws/api/v1'"

    def test_to_dict(self):
        """Test the to_dict functions correctly."""
        endpoint = AbstractEndpoint
        setattr(endpoint, "test_str", "str")
        setattr(
            endpoint,
            "datetime",
            datetime.strptime("2021-02-05T19:59:27.104+0000", "%Y-%m-%dT%H:%M:%S.%f%z"),
        )

        endpoint_dict = {
            "test_str": "str",
            "datetime": "2021-02-05T19:59:27.104Z",
            "path": "https://pentest.ws/api/v1",
        }

        assert endpoint.to_dict(endpoint) == endpoint_dict


class TestEngagement:
    """Tests for the Engagement Endpoint."""

    @vcr.use_cassette("tests/vcr_cassettes/engagement-create-200.yml")
    def test_engagement_create_200(self, engagement_dict_no_archived):
        """Test an API call to create an Engagement."""
        del engagement_dict_no_archived["id"]
        del engagement_dict_no_archived["created_at"]

        engagement = Engagement(**engagement_dict_no_archived)

        message = engagement.create()

        engagement_dict_no_archived["id"] = "za4Kz7oy"

        assert isinstance(engagement, Engagement)
        assert engagement.to_dict() == engagement_dict_no_archived
        assert message == "Engagement Engagement 1 (za4Kz7oy) created."

    @vcr.use_cassette("tests/vcr_cassettes/engagement-create-400.yml")
    def test_engagement_create_400(self, engagement_dict_no_archived):
        """Test an API call to create an Engagement with missing object."""
        del engagement_dict_no_archived["id"]
        del engagement_dict_no_archived["created_at"]

        engagement = Engagement(**engagement_dict_no_archived)

        setattr(engagement, "test_str", "str")
        delattr(engagement, "name")

        message = engagement.create()

        assert isinstance(engagement, Engagement)
        assert message == "Error: Missing name"

    @vcr.use_cassette("tests/vcr_cassettes/engagement-del-200.yml")
    def test_engagement_delete_200(self, engagement_object_no_archived):
        """Test an API call to get an Engagement."""
        engagement = engagement_object_no_archived

        message = engagement.delete()

        assert message == "Engagement Engagement 1 (7aBB7za9) deleted."

    @vcr.use_cassette("tests/vcr_cassettes/engagement-del-400.yml")
    def test_engagement_delete_400(self, engagement_object_no_archived):
        """Test an API call to get an Engagement."""
        engagement = engagement_object_no_archived

        message = engagement.delete()

        assert message == "Error: Engagement Engagement 1 (7aBB7za9) not found"

    @vcr.use_cassette("tests/vcr_cassettes/engagement-get.yml")
    def test_engagement_get(self, engagement_dict_no_archived):
        """Test an API call to get an Engagement."""
        engagement = Engagement.get("Engagement 1")

        assert isinstance(engagement, Engagement)
        assert engagement.to_dict() == engagement_dict_no_archived

    @vcr.use_cassette("tests/vcr_cassettes/engagement-get-all.yml")
    def test_engagement_get_eid(self):
        """Test an API call to get a specific Engagement."""
        eid = Engagement.get_eid("Engagement 1")

        assert isinstance(eid, str)
        assert eid == "7aBB7za9", "The eid should be 7aBB7za9."

    @vcr.use_cassette("tests/vcr_cassettes/engagement-get-all.yml")
    def test_engagement_get_all(self):
        """Test an API call to get all Engagement."""
        engagements = Engagement.get_all()

        assert isinstance(engagements, list)
        assert len(engagements) == 2, "The length should be 2."

    def test_engagement_to_dict_no_archived(
        self,
        engagement_dict_no_archived,
        engagement_keys,
        engagement_object_no_archived,
    ):
        """Tests engagement is correctly returned as a dictionary."""
        assert isinstance(engagement_object_no_archived, Engagement)
        assert engagement_object_no_archived.to_dict() == engagement_dict_no_archived

    def test_engagement_to_dict_no_created_at(
        self,
        engagement_dict_no_created_at,
        engagement_keys,
        engagement_object_no_created_at,
    ):
        """Tests engagement is correctly returned as a dictionary."""
        assert isinstance(engagement_object_no_created_at, Engagement)
        assert (
            engagement_object_no_created_at.to_dict() == engagement_dict_no_created_at
        )

    @vcr.use_cassette("tests/vcr_cassettes/engagement-update-200.yml")
    def test_engagement_update_200(self, engagement_dict_no_archived):
        """Test an API call to update an Engagement."""
        engagement = Engagement(**engagement_dict_no_archived)
        delattr(engagement, "client_id")
        engagement.notes = "Updated"
        engagement.archived = ""
        message = engagement.update()

        assert isinstance(engagement, Engagement)
        assert message == "Engagement Engagement 1 (7aBB7za9) updated."

    @vcr.use_cassette("tests/vcr_cassettes/engagement-update-400.yml")
    def test_engagement_update_400(self, engagement_dict_no_archived):
        """Test an API call to create an Engagement with missing object."""
        engagement = Engagement(**engagement_dict_no_archived)
        engagement.client_id = "123"
        engagement.archived = ""

        message = engagement.update()

        assert isinstance(engagement, Engagement)
        assert message == "Error: Invalid client_id"
