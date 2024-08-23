import aiohttp

from api_24ur import exceptions
from api_24ur import scraper
from api_24ur import types


async def get_post(url: str) -> types.Post:
    if not url.startswith('https://www.24ur.com/'):
        raise exceptions.InputException('Invalid URL')
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise exceptions.ServerSideError(f'Unexpected response code {response.status}')
            
            html = await response.text()

    return scraper.Scraper(html).scrape()
