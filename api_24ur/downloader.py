import io
import logging
import os
import shutil
import sys
import uuid

import aiohttp

try:
    from m3u8downloader import main as m3u8
except ImportError as e:
    raise RuntimeError('Download dependencies not installed, please install them') from e

from api_24ur import exceptions


# Monkeypath lib
def get_local_file_for_url(tempdir, url, path_line=None):
    if path_line and path_line.startswith(tempdir):
        return path_line
    path = m3u8.get_url_path(url)
    if path.startswith("/"):
        path = path[1:]

    # Limit file name length
    ext = path.split('.')[-1]
    path = f'{path[:250]}.{ext}'

    return os.path.normpath(os.path.join(tempdir, path))


m3u8.get_local_file_for_url = get_local_file_for_url
m3u8.logger.handlers = [logging.NullHandler()]
m3u8.logger.propagate = False


class Downloader:
    def __init__(
        self,
        url: str,
        download_path: str = '/tmp',
        tmp_dir: str = '/tmp',
        pool_size: int = 5,
        max_bitrate: int = sys.maxsize,
    ) -> None:
        self.url = url
        self.download_path = download_path
        self.tmp_dir = tmp_dir
        self.pool_size = pool_size
        self.max_bitrate = max_bitrate

    async def download(self) -> str:
        output_file_path = f'{self.download_path}/{uuid.uuid4()}.mp4'

        downloader = m3u8.M3u8Downloader(
            url=await self._find_suitable_stream(),
            output_filename=output_file_path,
            tempdir=self.tmp_dir,
        )
        downloader.start()

        # Cleanup
        shutil.rmtree(path=downloader.tempdir, ignore_errors=True)

        return output_file_path

    async def download_bytes(self) -> io.BytesIO:
        fp = await self.download()
        with open(fp, 'rb') as f:
            bytes = io.BytesIO(f.read())

        os.remove(fp)
        return bytes

    async def _find_suitable_stream(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.url,
            ) as response:
                data = (await response.text()).split('\n')

        stream, bitrate = None, 0
        for i in range(0, len(data), 2):
            for part in data[i].split(','):
                key, _, val = part.partition('=')
                if key == 'BANDWIDTH' and int(val) > bitrate and int(val) <= self.max_bitrate:
                    bitrate = int(val)
                    stream = data[i + 1]

        if not stream:
            raise exceptions.DownloadException('No suitable stream found')

        return stream
