import typing
import uuid

import aiohttp

from api_24ur import schemas
from api_24ur import types


ARTICLE_API_URL = 'https://gqlc.24ur.com/graphql/?raw=&query=onl_web_full_article(url:%20%22{path}%22)'
ARTICLE_HEADERS = {
    'host': 'gqlc.24ur.com',
    'accept-encoding': 'gzip',
}

GRAPH_API_URL = 'https://gql.24ur.si/graphql'
GRAPH_API_HEADERS = {
    'accept-encoding': 'gzip',
    'content-type': 'application/graphql; charset=utf-8',
    'host': 'gql.24ur.si',
}
VIDEO_STREAM_PAYLOAD = '{{videoHlsUrl(id: {video_id}, siteId: 1) {{url info infoCode}}}}'
COMMENTS_PAYLOAD = '{{ comments(itemType: ARTICLE, itemId: {article_id}, perPage: {limit}, nextId: "") {{ total totalShown nextId comments {{ id createdOn body owner {{ id nickname avatarUrl }} likes {{ sum negative positive }} replies {{ id body createdOn owner {{ id nickname avatarUrl }} likes {{ sum negative positive }}}}}}}}}}'  # noqa: E501

DEFAULT_USER_AGENT = '24ur Android App 4.4.1 (168)'


class Client:
    def __init__(
        self,
        user_agent: typing.Optional[str] = None,
        device_id: typing.Optional[str] = None,
        authorization: typing.Optional[str] = None,
    ) -> None:
        self._article_headers = ARTICLE_HEADERS | {
            'device-id': device_id or str(uuid.uuid4()),
            'authorization': authorization or '',
            'user-agent': user_agent or DEFAULT_USER_AGENT,
        }
        self._graph_headers = GRAPH_API_HEADERS | self._article_headers

    async def get_article_by_url(self, url: str, image_size_px: int = 1200) -> types.Article:
        """
        Fetches article by URL
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=ARTICLE_API_URL.format(path=self._path_from_url(url)),
                headers=self._article_headers,
            ) as response:
                data = await response.json()

        article = schemas.Root.from_dict(data).data.article
        return article

    async def _fetch_video_stream_url(self, video_id: int) -> str:
        request_body = VIDEO_STREAM_PAYLOAD.format(video_id=video_id)
        headers = self._graph_headers | {'content-length': str(len(request_body))}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=GRAPH_API_URL,
                data=request_body,
                headers=headers,
            ) as response:
                data = await response.json()

        return schemas.VideoHls.from_dict(data.get('data', {}).get('videoHlsUrl', {})).url

    async def _get_comments(self, article_id: int, limit: int = 1000) -> typing.List[schemas.Comment]:
        request_body = COMMENTS_PAYLOAD.format(article_id=article_id, limit=limit)
        headers = self._graph_headers | {'content-length': str(len(request_body))}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=GRAPH_API_URL,
                data=request_body,
                headers=headers,
            ) as response:
                data = await response.json()

        return [
            schemas.Comment.from_dict(comment)
            for comment in data.get('data', {}).get('comments', {}).get('comments', [])
        ]

    def _path_from_url(self, url: str) -> str:
        return url.split('?')[0].split('.com')[1]
