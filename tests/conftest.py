"""pytest plugin configuration.

https://docs.pytest.org/en/latest/writing_plugins.html#conftest-py-plugins
"""
# Third-Party Libraries
import pytest

# Custom Libraries
from pws_api_wrapper.engagement import Engagement


def pytest_addoption(parser):
    """Add new commandline options to pytest."""
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    """Register new markers."""
    config.addinivalue_line("markers", "slow: mark test as slow")


def pytest_collection_modifyitems(config, items):
    """Modify collected tests based on custom marks and commandline options."""
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture
def engagement_dict_no_archived():
    """Return an Engagement Dictionary."""
    return {
        "id": "7aBB7za9",
        "name": "Engagement 1",
        "notes": "<strong>Test 1</strong>",
        "client_id": "",
        "created_at": "2021-02-05T19:59:27.104Z",
    }


@pytest.fixture
def engagement_dict_no_created_at():
    """Return an Engagement Dictionary."""
    return {
        "id": "7aBB7za9",
        "name": "Engagement 1",
        "notes": "<strong>Test 1</strong>",
        "client_id": "",
        "archived": "2021-02-05T19:59:27.104Z",
    }


@pytest.fixture
def engagement_keys():
    """Responsible only for returning the test data."""
    return ["id", "name", "notes", "client_id", "created_at", "archived"]


@pytest.fixture
def engagement_object_no_archived():
    """Return an Engagement Object."""
    return Engagement(
        id="7aBB7za9",
        name="Engagement 1",
        notes="<strong>Test 1</strong>",
        created_at="2021-02-05T19:59:27.104Z",
    )


@pytest.fixture
def engagement_object_no_created_at():
    """Return an Engagement Object."""
    return Engagement(
        id="7aBB7za9",
        name="Engagement 1",
        notes="<strong>Test 1</strong>",
        archived="2021-02-05T19:59:27.104Z",
    )


@pytest.fixture
def host_dict():
    """Return a Host dictionary."""
    return {
        "target": "1.2.3.4",
        "board_id": "abcd1234",
        "eid": "ZaAvk46j",
        "flagged": True,
        "hostnames": "host",
        "id": "No3e25l6",
        "label": "label",
        "notes": "Note",
        "os": "OS",
        "os_type": "Linux",
        "out_of_scope": True,
        "owned": False,
        "reviewed": True,
        "shell": True,
        "thumbs_down": True,
        "thumbs_up": True,
        "type": "Unknown",
    }


@pytest.fixture
def port_dict():
    """Return a Port dictionary."""
    return {
        "id": "56VqkKba",
        "hid": "za4AlEP6",
        "port": 22,
        "proto": "tcp",
        "service": "SSH",
        "version": "2.3",
        "status": "Needs Review",
        "state": "open",
        "notes": "Some Notes",
        "checklist": [{"0": "Log In?"}],
    }


@pytest.fixture
def scratchpad_dict():
    """Return a Scratchpad dictionary."""
    return {
        "id": "1abWR16y",
        "hid": "za4AlEP6",
        "title": "README.md",
        "type": "code",
        "language": "markdown",
        "content": "`hash:user``",
    }
