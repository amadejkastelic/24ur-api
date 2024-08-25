import datetime
import io
import sys
import typing
import uuid

import aiohttp

from api_24ur import downloader
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

    async def get_article_by_url(
        self,
        url: str,
        num_comments: int = 0,
        image_size_px: int = 1200,
    ) -> types.Article:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=ARTICLE_API_URL.format(path=self._path_from_url(url)),
                headers=self._article_headers,
            ) as response:
                data = await response.json()

        article = schemas.Root.from_dict(data).data.article

        return types.Article(
            id=article.id,
            author=article.source,
            title=article.title,
            summary=article.summary,
            content='\n'.join([item.body if item.body else '' for item in article.body_items or []]),
            place=article.place,
            num_views=article.nb_views,
            posted_at=datetime.datetime.fromtimestamp(article.date) if article.date else None,
            images=[
                types.Image(
                    caption=image.caption,
                    url=image.src.replace('PLACEHOLDER', f'{image_size_px}xX'),
                    height=image.height,
                    width=image.width,
                )
                for image in article.images or []
            ],
            videos=[
                types.Video(
                    title=video.title,
                    url=await self._fetch_video_stream_url(video.id),
                )
                for video in article.videos
            ],
            comments=await self._fetch_comments(article_id=article.id, limit=num_comments) if num_comments > 0 else [],
        )

    async def download_video(
        self,
        stream_url: str,
        download_path: str = '/tmp',
        tmp_dir: str = '/tmp',
        pool_size: int = 5,
        max_bitrate: int = sys.maxsize,
    ) -> str:
        await downloader.Downloader(
            url=stream_url,
            download_path=download_path,
            tmp_dir=tmp_dir,
            pool_size=pool_size,
            max_bitrate=max_bitrate,
        ).download()

    async def download_video_bytes(
        self,
        stream_url: str,
        tmp_dir: str = '/tmp',
        pool_size: int = 5,
        max_bitrate: int = sys.maxsize,
    ) -> io.BytesIO:
        return await downloader.Downloader(
            url=stream_url,
            download_path=tmp_dir,
            tmp_dir=tmp_dir,
            pool_size=pool_size,
            max_bitrate=max_bitrate,
        ).download_bytes()

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

    async def _fetch_comments(self, article_id: int, limit: int = 1000) -> typing.List[types.Comment]:
        request_body = COMMENTS_PAYLOAD.format(article_id=article_id, limit=limit)
        headers = self._graph_headers | {'content-length': str(len(request_body))}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=GRAPH_API_URL,
                data=request_body,
                headers=headers,
            ) as response:
                data = await response.json()

        return self._parse_comments(
            [
                schemas.Comment.from_dict(comment)
                for comment in data.get('data', {}).get('comments', {}).get('comments', [])
            ]
        )

    def _path_from_url(self, url: str) -> str:
        return url.split('?')[0].split('.com')[1]

    def _parse_comments(self, comments: typing.List[schemas.Comment]) -> typing.List[types.Comment]:
        return [
            types.Comment(
                author=comment.owner.nickname if comment.owner else 'Unknown',
                author_avatar_url=comment.owner.avatar_url if comment.owner else None,
                posted_at=datetime.datetime.fromtimestamp(comment.created_on) if comment.created_on else None,
                content=comment.body,
                likes=comment.likes.positive,
                dislikes=comment.likes.negative,
                score=comment.likes.sum,
                replies=self._parse_comments(comment.replies) if comment.replies else [],
            )
            for comment in comments
        ]
