#!/usr/bin/env pytest -vs
"""Tests for Host objects in pws-api-wrapper."""

# Third-Party Libraries
import pytest
from schema import SchemaError
import vcr

# Custom Libraries
from pws_api_wrapper import Host


class TestHost:
    """Tests for the Host Endpoint."""

    @pytest.mark.parametrize(
        "target",
        [
            "1.2.3.4",
            "2001:db8:85a3::8a2e:370:7334",
            "2001:db8:85a3:1234:1234:8a2e:370:7334",
        ],
    )
    def test_init_validation_pass(self, target, host_dict):
        """Test the init validation."""
        host_dict["target"] = target

        host = Host(**host_dict)

        assert host.to_dict() == host_dict

    @pytest.mark.parametrize(
        "attribute,value,error_message",
        [
            ("board_id", 4, '"board_id" should be 8 alphanumeric characters'),
            ("board_id", "asd123", '"board_id" should be 8 alphanumeric characters'),
            ("board_id", "abcd123!", '"board_id" should be 8 alphanumeric characters'),
            ("eid", 4, '"eid" should be 8 alphanumeric characters'),
            ("eid", "asd123", '"eid" should be 8 alphanumeric characters'),
            ("eid", "abcd123!", '"eid" should be 8 alphanumeric characters'),
            ("flagged", 1, '"flagged" should be True/False boolean'),
            ("hostnames", 1, '"hostnames" should be a string'),
            ("id", 4, '"id" should be 8 alphanumeric characters'),
            ("id", "asd123", '"id" should be 8 alphanumeric characters'),
            ("id", "abcd123!", '"id" should be 8 alphanumeric characters'),
            ("label", 1, '"label" should be a string'),
            ("notes", 1, '"notes" should be a string'),
            ("os", 1, '"os" should be a string'),
            ("os_type", 1, 'Not a valid "os_type".'),
            ("os_type", "other", 'Not a valid "os_type".'),
            ("out_of_scope", 1, '"out_of_scope" should be True/False boolean'),
            ("owned", 1, '"owned" should be True/False boolean'),
            ("reviewed", 1, '"reviewed" should be True/False boolean'),
            ("shell", "1", '"shell" should be True/False boolean'),
            ("thumbs_down", 2, '"thumbs_down" should be True/False boolean'),
            ("thumbs_up", 1, '"thumbs_up" should be True/False boolean'),
            ("type", 1, 'Not a valid "type".'),
            ("type", "Something", 'Not a valid "type".'),
        ],
    )
    def test_init_validation_fail(self, attribute, value, error_message, host_dict):
        """Test the init validation fails when string value are not strings."""
        host_dict[attribute] = value
        with pytest.raises(SchemaError, match=error_message):
            Host(**host_dict)

    @pytest.mark.parametrize(
        "value",
        [
            ("456.1.1.1"),
            ("1.456.1.1"),
            ("1.1.456.1"),
            ("1.1.1.456"),
            ("1.2.3.4.5"),
            ("2456.1.1.1"),
            ("1.2456.1.1"),
            ("1.1.2456.1"),
            ("1.1.1.2456"),
            ("test"),
            (""),
            (1),
            ("2001:0db8:85a3:0000:0000:8a2e:0370:7334:asdf"),
        ],
    )
    def test_init_validation_target_fail(self, value, host_dict):
        """Test the init validation fails when string value are not strings."""
        host_dict["target"] = value
        with pytest.raises(SchemaError, match="Target should be a valid IPv4 Address"):
            Host(**host_dict)

    @vcr.use_cassette("tests/vcr_cassettes/host-create-200.yml")
    def test_create_200(self, host_dict):
        """Test an API call to create an Engagement."""
        # Delete board_id as it does not appear to come from the API yet.
        # FIXME This should be removed once the API returns it.
        del host_dict["board_id"]

        # Delete id as the API will not accept when creating.
        del host_dict["id"]

        host = Host(**host_dict)

        message = host.create()

        # Add host ID back to host_dict
        host_dict["id"] = host.id

        assert isinstance(host, Host)
        assert host.to_dict() == host_dict
        assert message == "Host 1.2.3.4 (No3e25l6) created."

    @vcr.use_cassette("tests/vcr_cassettes/host-del-200.yml")
    def test_host_delete_200(self, host_dict):
        """Test an API call to delete a Host."""
        host = Host(**host_dict)

        message = host.delete()

        assert message == "Host 1.2.3.4 (No3e25l6) deleted."

    @vcr.use_cassette("tests/vcr_cassettes/host-del-400.yml")
    def test_host_delete_400(self, host_dict):
        """Test an API call to delete an Host that fails."""
        host = Host(**host_dict)
        host.id = "abdc1234"

        message = host.delete()

        assert message == "Error: Host 1.2.3.4 (abdc1234) not found"

    @vcr.use_cassette("tests/vcr_cassettes/host-create-400.yml")
    def test_engagement_create_400(self, host_dict):
        """Test an API call to create an Engagement with missing object."""
        host = Host(**host_dict)

        message = host.create()

        assert isinstance(host, Host)
        assert message == "Error: Invalid board_id: abcd1234"

    @vcr.use_cassette("tests/vcr_cassettes/host-get-200.yml")
    def test_get_200(self, host_dict):
        """Test an API call to get a host."""
        host = Host.get("No3e25l6")

        assert isinstance(host, Host)
        assert host.to_dict() == host_dict

    @vcr.use_cassette("tests/vcr_cassettes/host-get-400.yml")
    def test_get_400(self):
        """Test an API call to get a host that returns an error."""
        with pytest.raises(SystemExit):
            Host.get("abcd1234")

    @vcr.use_cassette("tests/vcr_cassettes/host-get-all.yml")
    def test_get_all(self, engagement_object_no_archived):
        """Test an API call to get all hosts for an Engagement."""
        host = Host.get_all(engagement_object_no_archived.id)

        assert len(host) == 3

    @vcr.use_cassette("tests/vcr_cassettes/host-update-200.yml")
    def test_update_200(self, host_dict):
        """Test an API call to put an update to a Host."""
        host_dict["label"] = "New Label"

        # FIXME This should be removed once the API returns it.
        del host_dict["board_id"]

        host = Host(**host_dict)

        message = host.update()

        assert isinstance(host, Host)
        assert host.to_dict() == host_dict
        assert message == "Host 1.2.3.4 (No3e25l6) updated."

    @vcr.use_cassette("tests/vcr_cassettes/host-update-400.yml")
    def test_host_update_400(self, host_dict):
        """Test an API call to create an Host with missing object."""
        host = Host(**host_dict)

        message = host.update()

        assert isinstance(host, Host)
        assert message == "Error: Invalid board_id: abcd1234"
