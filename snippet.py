import asyncio

from api_24ur import client


print(
    asyncio.run(
        client.Client()._get_comments(
            article_id=4430772,
            limit=1000,
        )
    )
)
