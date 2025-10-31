import asyncio
import os
import requests
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_24ur import client  # noqa: E402


async def main():
    cl = client.Client()

    article_url = input('Enter the article URL: ')

    article = await cl.get_article_by_url(article_url, num_comments=5)
    print(f'Article: {article}')

    if article.videos:
        media_path = await cl.download_video(
            stream_url=article.videos[0].url,
            download_path='.',
        )
        print(f'Video downloaded to: {media_path}')
    elif article.images:
        response = requests.get(article.images[0].url).content
        with open('image.jpg', 'wb') as f:
            f.write(response)
        media_path = os.path.abspath('image.jpg')
        print(f'Image downloaded to: {media_path}')


if __name__ == '__main__':
    asyncio.run(main())
