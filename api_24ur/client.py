import typing
import uuid

import aiohttp

from api_24ur import types


API_URL = 'https://gqlc.24ur.com/graphql/?raw=&query=onl_web_full_article(url:%20%22{path}%22)'
DEFAULT_USER_AGENT = '24ur Android App 4.4.1 (168)'
DEFAULT_HEADERS = {
    'host': 'gqlc.24ur.com',
    'accept-encoding': 'gzip',
}


class Client:
    def __init__(
        self,
        user_agent: typing.Optional[str] = None,
        device_id: typing.Optional[str] = None,
        authorization: typing.Optional[str] = None,
    ) -> None:
        self._headers = DEFAULT_HEADERS | {
            'device-id': device_id or str(uuid.uuid4()),
            'authorization': authorization or '',
            'user-agent': user_agent or DEFAULT_USER_AGENT,
        }

    async def get_article_by_url(self, url: str) -> types.Article:
        """
        Fetches article by URL
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL.format(path=self._path_from_url(url))) as response:
                print(API_URL.format(path=self._path_from_url(url)))
                data = await response.json()

        return types.Root.from_dict(data).data.article

    def _path_from_url(self, url: str) -> str:
        return url.split('?')[0].split('.com')[1]
