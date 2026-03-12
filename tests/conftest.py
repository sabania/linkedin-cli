"""Shared fixtures for LinkedIn CLI tests.

All test data is derived dynamically from the logged-in user.
Run `linkedin-cli login` before running tests.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from auth import get_client


@pytest.fixture(scope="session")
def api():
    """Shared LinkedIn client (one browser session for all tests)."""
    client = get_client()
    yield client
    client.quit()


@pytest.fixture(scope="session")
def me(api):
    """Logged-in user's profile."""
    return api.get_user_profile()


@pytest.fixture(scope="session")
def my_public_id(me):
    """Public profile ID of logged-in user."""
    return me.get("miniProfile", {}).get("publicIdentifier", "")


@pytest.fixture(scope="session")
def my_posts(api, my_public_id):
    """First 3 posts of the logged-in user."""
    return api.get_profile_posts(public_id=my_public_id, post_count=3)


@pytest.fixture(scope="session")
def first_post_urn(my_posts):
    """URN of the user's most recent post (or None)."""
    if my_posts:
        return my_posts[0].get("urn", "")
    return ""


@pytest.fixture(scope="session")
def first_post_activity_id(first_post_urn):
    """Activity ID extracted from the first post URN."""
    if first_post_urn:
        return first_post_urn.split(":")[-1]
    return ""


@pytest.fixture(scope="session")
def my_urn_id(me):
    """URN ID of the logged-in user (e.g. ACoAAB9VU90B...)."""
    urn = me.get("miniProfile", {}).get("entityUrn", "")
    # Extract the ID part from urn:li:fs_miniProfile:ACoAAB9VU90B...
    return urn.split(":")[-1] if urn else ""


@pytest.fixture(scope="session")
def my_first_name(me):
    """First name of the logged-in user."""
    return me.get("miniProfile", {}).get("firstName", "")


@pytest.fixture(scope="session")
def my_last_name(me):
    """Last name of the logged-in user."""
    return me.get("miniProfile", {}).get("lastName", "")


@pytest.fixture(scope="session")
def cli_app():
    """Import the CLI app."""
    from main import app
    return app
