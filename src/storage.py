import os

from azure.storage.queue import QueueClient

conn_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")


def load_queue(connection_string: str, name: str, **kwargs) -> QueueClient:
    """
    source: https://learn.microsoft.com/en-us/azure/storage/queues/storage-python-how-to-use-queue-storage?tabs=python%2Cenvironment-variable-windows
    **kwargs are passed to the QueueClient connection and should be valid kwargs for the QueueClient
    """
    # Create a unique name for the queue
    return QueueClient.from_connection_string(connection_string, name, **kwargs)
