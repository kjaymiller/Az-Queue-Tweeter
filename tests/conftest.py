from dataclasses import dataclass

import azure.storage.queue
import pytest

from src import queuetweeter, storage, twitter


@pytest.fixture(scope="session")
def test_storage_auth():
    return storage.Auth(
        queue_name="test-messages", connection_string="test_connection_string"
    )


@pytest.fixture(scope="session")
def test_twitter_auth():
    return twitter.Auth(
        consumer_key="Foo",
        consumer_secret="Bar",
        access_token="Biz",
        access_token_secret="Baz",
    )


@dataclass
class Media:
    media_id: int
    media_id_string: str


@pytest.fixture()
def test_media():
    return Media(123457890, "123457890")


class MockItemPaged:
    def next(self):
        return azure.storage.queue.QueueMessage(content="test")


class MockQueue:
    def receive_messages(self):
        return MockItemPaged()

    def send_message(self, txt):
        pass

    def delete_message(self, msg_id, msg_receipt):
        pass


@pytest.fixture()
def test_queue_tweeter(mocker, test_storage_auth, test_twitter_auth):
    mocker.patch.object(storage.Auth, "Client", MockQueue())
    return queuetweeter.QueueTweeter(
        storage_auth=test_storage_auth, twitter_auth=test_twitter_auth
    )
