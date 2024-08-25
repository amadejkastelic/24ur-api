# Unofficial 24ur API Client

## Installation

```bash
pip install 24ur-api
```
- With video download support
```bash
pip install 24ur-api[download]
```

## Usage

```python
from 24ur_api import client

24ur_client = client.Client()

# Get article by URL with 10 comments
article = await client.get_article_by_url(url='<article_url>', num_comments=10)

# Download the first video of article with bitrate lower than 2000000b to current dir
await client.download_video(stream_url=article.videos[0].url, download_path='.', max_bitrate=2000000)
# Or get bytes
await client.download_video_bytes(stream_url=article.videos[0].url, max_bitrate=2000000)
```
