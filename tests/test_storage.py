import logging
from unittest.mock import Mock

import pytest
from tweepy import API, Client

import src
from src.storage import Auth


@pytest.mark.parametrize(
    "env_key,class_key,env_val",
    [
        ("AZURE_STORAGE_CONNECTION_STRING", "connection_string", "test_connection_string"),
    ],
)
def test_auth_from_environ(monkeypatch, env_key, class_key, env_val):
    """Tests that you can pass in the auth credentials as environment variables."""

    monkeypatch.setenv(env_key, env_val)

    auth = Auth(queue_name='message-queue')
    assert getattr(auth, class_key) == env_val


@pytest.mark.parametrize(
    "env_key,env_param",
    [
        ("AZURE_STORAGE_CONNECTION_STRING", "connection_string"),
    ],
)
def test_empty_auth_warning_raised(caplog, monkeypatch, env_key, env_param):
    """Tests that a warning is raised if a value is not found"""

    caplog.set_level(logging.WARNING)
    monkeypatch.delenv(env_key, raising=False)

    auth = Auth(queue_name='message-queue')
    assert any([env_param in x.message for x in caplog.records])


def test_Auth_has_client(test_auth):
    """assert that Auth has a Client property. MyPy will enforce type"""

    assert test_auth.Client