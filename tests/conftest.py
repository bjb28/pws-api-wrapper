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
def finding_dict():
    """Return a Finding dictionary."""
    return {
        "id": "abdc1234",
        "eid": "46yEw36g",
        "finding_id": "01",
        "title": "Test Finding",
        "environment": "Web App",
        "category": "Injection",
        "risk_level": "Critical",
        "cvss2_num": 5.5,
        "cvss2_str": "AV:N/AC:L/Au:S/C:P/I:P/A:N",
        "cvss3_num": 6.4,
        "cvss3_str": "AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:N",
        "dread": [
            "9  Admin data",
            "10 Very easy",
            "9  Simple proxy",
            "10 All users",
            "5  HTTP requests",
        ],
        "background": "html",
        "desc_brief": "html",
        "desc_full": "html",
        "impact_brief": "html",
        "impact_full": "html",
        "reco_brief": "html",
        "reco_full": "html",
        "reco_effort": "html",
        "targets": "html",
        "references": "html",
        "evidence": "html",
        "validation_steps": "html",
        "remediation_log": "html",
    }


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
def notePage_dict():
    """Return a Note Page dictionary."""
    return {
        "id": "1ab5Mqoy",
        "oid": "46yEw36g",
        "otype": "e",
        "title": "Engagement Test Note",
        "content": "Some text is here.",
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
