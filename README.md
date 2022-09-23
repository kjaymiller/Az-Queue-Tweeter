# AZImageTweeter

Send images to Twitter using text from Azure Queue Storage

## Example usage

```
from PIL import Image

from storage import load_queue
from twitter import send_tweet

queue = load_queue("31daysofndqueue")

img = Image.open("hopper.jpg")
img_bytes = BytesIO()
img.save(img_bytes, format="JPEG")

api = tweepy.API(tweepy.OAuth1UserHandler(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
))
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)

send_tweet(image=image, text="Hello world!", client=client, api=api)
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


