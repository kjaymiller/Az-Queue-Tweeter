# AZ-Queue-Tweeter

Send images to Twitter using text from Azure Queue Storage

## Installation

Install via PyPI
`pip install azqueuetweeter`

## Usage instructions

### Setup Azure authentication:

First, as a general rule, you should not store credentials in your code;
a better option is to store them in environment variables and retrieve them
with `os.environ.get('ENV_NAME')`.

Here's what you'll need for Azure storage authentication:

```
from azqueuetweeter import storage

sa = storage.Auth(connection_string="CONNECTION-STRING", queue_name="YOUR-QUEUE-NAME")
```

The `connection_string` comes from [the Azure portal](https://learn.microsoft.com/en-us/azure/storage/queues/storage-python-how-to-use-queue-storage?tabs=python%2Cenvironment-variable-windows#copy-your-credentials-from-the-azure-portal).
The `queue_name` is whatever your named your queue. You can either create that programmatically
using the Azure client library, or more easily, using the [Azure Storage Explorer app](https://learn.microsoft.com/en-us/azure/vs-azure-tools-storage-manage-with-storage-explorer?tabs=macos).

### Setup Twitter authentication:

You'll need a few more details for Twitter authentication:

```
from azqueuetweeter import twitter

ta = twitter.Auth(
    consumer_key='CONSUMER-KEY',
    consumer_secret='CONSUMER-SECRET',
    access_token='ACCOUNT-ACCESS-TOKEN',
    access_token_secret='ACCOUNT-ACCESS-TOKEN-SECRET')
```

The `consumer_key` is also known as the API key and is provided to you in the Twitter developer portal. Similarly, the `consumer_secret` is also known as the API secret and is provided in the same place.

The `access_token` and `access_token_secret` credentials are for the Twitter account that will actually be the tweet author. If you're sending from the same account as the one that signed up for Twitter API access, then you can get those strings from the Twitter developer portal.If you're sending from a different account, you will need to do 3-legged OAuth to get that account's credentials.

To do 3-legged OAuth, first complete the _User authentication set up_ on the app settings page in the Twitter developer portal. Then use the `tweepy` package to programmatically go through the flow.

First, get an authorization URL for your app:

```
>>> oauth1_user_handler = tweepy.OAuth1UserHandler(
    "CONSUMER-KEY", "CONSUMER-SECRET",
    callback="http://pamelafox.github.io"
)
>>> print(oauth1_user_handler.get_authorization_url())
https://api.twitter.com/oauth/authorize?oauth_token=OAUTH-TOKEN
```

Then visit that URL using the desired account for tweeting,
confirm authorization of the app, and see the app redirect to a URL like:

https://registeredwebsite.com/?oauth_token=OAUTH-TOKEN&oauth_verifier=OAUTH_VERIFIER

Put the `OAUTH-VERIFIER` value into the next call:

```
access_token, access_token_secret = oauth1_user_handler.get_access_token(
    "OAUTH-VERIFIER"
)
```

Now you have the `access_token` and `access_token_secret` needed for the `twitter.Auth` constructor above.

### Construct a Queue Tweeter

Construct a `QueueTweeter` using the authentication objects:

```
from azqueuetweeter import QueueTweeter
qt = QueueTweeter(storage_auth=sa, twitter_auth=ta)
```

### Queue up messages

You can add messages to the Queue either manually with the Azure Storage Explorer app or programmatically using the `QueueTweeter.queue_message` method.

To queue up a message with a simple string:

```
qt.queue_message('Hello world!')
```

You might also find it useful to queue up stringified JSON:

```
import json
qt.queue_message(json.dumps({"text": "Whats your fav Python web framework?", "poll_options": ["Flask", "Django", "FastAPI", "All of em!"], "poll_duration_minutes": 60*24}))
```

Later, you can transform your queued messages into tweet content, so you can store the information in the queue however works for you.

### Send messages as tweets

Now you can send tweets using the `QueueTweeter.send_next_message` method.

If the queued message contains exactly the text that you want tweeted, then you can call it with no arguments:

```
qt.send_next_message()
```

To confirm the tweet contents first, you can specify `preview_mode=True` :

```
qt.send_next_message(preview_mode=True)
```

To transform the queued message content first, specify a `message_transformer` function that returns back
a dict with the same arguments as tweepy's [create_tweet](https://docs.tweepy.org/en/stable/client.html#tweepy.Client.create_tweet) function. The most important argument is `"text"` but many other arguments are also possible.

This example adds a hashtag to the queued message string:

```
qt.send_next_message(message_transformer=lambda msg: {"text": msg + " #Python"})
```

This example deserializes a serialized JSON string message:

```
import json

qt.queue_message(json.dumps({"text": "Whats your fav Python web framework?", "poll_options": ["Flask", "Django", "FastAPI", "All of em!"], "poll_duration_minutes": 60*24}))
qt.send_next_message(message_transformer=lambda msg: json.loads(msg))
```

It's also possible to upload an image to the tweet, as long as your Twitter account is approved for "elevated access".
Your `message_transformer` must return the image bytes in a `"file"` key and provide a filename (with an extension)
in the `"filename"` key..

```

import io
from PIL import Image

img = Image.open("Python_logo_icon.png")
img_bytes = io.BytesIO()
img.save(img_bytes, format="PNG")
img_bytes.seek(0)

qt.queue_message("I want a stuffed Python logo!")
qt.send_next_message(preview_mode=False, message_transformer=lambda msg: {"text": msg, "filename": "python.jpg", "file": img_bytes})
```

## Development guide

Start a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

Install poetry:

```
python -m pip install poetry
```

Install project dependencies:

```
poetry install
```
