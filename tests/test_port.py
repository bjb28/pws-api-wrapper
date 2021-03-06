#!/usr/bin/env pytest -vs
"""Tests for Port objects in pws-api-wrapper."""

# Third-Party Libraries
import pytest
from schema import SchemaError
import vcr

# Custom Libraries
from pws_api_wrapper import Port


class TestPort:
    """Tests for the Port Endpoint."""

    def test_init_validation_pass(self, port_dict):
        """Test the init validation."""
        port = Port(**port_dict)

        assert port.to_dict() == port_dict

    @pytest.mark.parametrize(
        "attribute,value,error_message",
        [
            ("id", 4, '"id" should be 8 alphanumeric characters'),
            ("id", "abc1234", '"id" should be 8 alphanumeric characters'),
            ("id", "abcd123$", '"id" should be 8 alphanumeric characters'),
            ("hid", 4, '"hid" should be 8 alphanumeric characters'),
            ("hid", "abc1234", '"hid" should be 8 alphanumeric characters'),
            ("hid", "abcd123$", '"hid" should be 8 alphanumeric characters'),
            ("port", -1, '"port" should be an intiger between 0 and 65,535.'),
            ("port", 65536, '"port" should be an intiger between 0 and 65,535.'),
            ("port", 1.2, '"port" should be an intiger between 0 and 65,535.'),
            ("port", "a", '"port" should be an intiger between 0 and 65,535.'),
            ("proto", "work", '"proto" should be "tcp", "udp", or None'),
            ("proto", 1, '"proto" should be "tcp", "udp", or None'),
            ("service", 1, '"service" should be a string'),
            ("version", 1, '"version" should be a string'),
            ("status", 1, 'Not a valid "status".'),
            ("status", "other", 'Not a valid "status".'),
            ("state", 1, 'Not a valid "state".'),
            ("state", "other", 'Not a valid "state".'),
            ("notes", 1, '"notes" should be a string'),
            ("checklist", "adf", '"checklist" should be a list of dictionaries.'),
        ],
    )
    def test_init_validation_fail(self, attribute, value, error_message, port_dict):
        """Test the init validation fails when incorrect values are provided."""
        port_dict[attribute] = value
        with pytest.raises(SchemaError, match=error_message):
            Port(**port_dict)

    @vcr.use_cassette("tests/vcr_cassettes/port/create-200.yml")
    def test_create_200(self, port_dict):
        """Test an API call to create a Port Object."""
        # Delete id as the API will not accept when creating.
        del port_dict["id"]

        port = Port(**port_dict)

        message = port.create()

        # Add port ID back to port_dict
        port_dict["id"] = port.id

        assert isinstance(port, Port)
        assert port.to_dict() == port_dict
        assert message == "Port 22 (za4AlEP6) created."

    @vcr.use_cassette("tests/vcr_cassettes/port/create-400.yml")
    def test_create_400(self, port_dict):
        """Test a failing API call to create a Port Object."""
        # Delete id as the API will not accept when creating.
        del port_dict["id"]
        # Delete change to a fake hid to cause 400 error.
        port_dict["hid"] = "abdc1234"

        port = Port(**port_dict)

        message = port.create()

        assert message == "Error: Invalid Host ID"

    @vcr.use_cassette("tests/vcr_cassettes/port/del-200.yml")
    def test_port_delete_200(self, port_dict):
        """Test an API call to delete a Port."""
        port = Port(**port_dict)

        message = port.delete()

        assert message == "Port 22 (56VqkKba) deleted."

    @vcr.use_cassette("tests/vcr_cassettes/port/del-404.yml")
    def test_port_delete_400(self, port_dict):
        """Test an API call to delete an Port that fails."""
        port = Port(**port_dict)
        port.id = "abdc1234"

        message = port.delete()

        assert message == "Error: Port 22 (abdc1234) not found"

    @vcr.use_cassette("tests/vcr_cassettes/port/get-200.yml")
    def test_get_200(self, port_dict):
        """Test an API call to get a port."""
        port = Port.get("56VqkKba")

        assert isinstance(port, Port)
        assert port.to_dict() == port_dict

    @vcr.use_cassette("tests/vcr_cassettes/port/get-400.yml")
    def test_get_400(self):
        """Test an API call to get a port that returns an error."""
        with pytest.raises(SystemExit):
            Port.get("abcd1234")

    @vcr.use_cassette("tests/vcr_cassettes/port/get-all-200.yml")
    def test_get_all(self, host_dict):
        """Test an API call to get all hosts for an Engagement."""
        ports = Port.get_all(host_dict["id"])

        assert len(ports) == 6

    @vcr.use_cassette("tests/vcr_cassettes/port/update-200.yml")
    def test_update_200(self, port_dict):
        """Test an API call to put an update to a Port."""
        port_dict["service"] = "New SSH"

        port = Port(**port_dict)

        message = port.update()

        assert isinstance(port, Port)
        assert port.to_dict() == port_dict
        assert message == "Port 22 (56VqkKba) updated."

    @vcr.use_cassette("tests/vcr_cassettes/port/update-400.yml")
    def test_host_update_400(self, port_dict):
        """Test an API call to create an Port with incorrect hid."""
        port = Port(**port_dict)

        message = port.update()

        assert isinstance(port, Port)
        assert message == "Error: Invalid Field: port"
