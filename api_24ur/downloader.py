import io
import os
import sys
import uuid

import yt_dlp
from yt_dlp import utils as yt_dlp_utils

from api_24ur import exceptions


class Downloader:
    def __init__(
        self,
        url: str,
        download_path: str = '/tmp',
        max_bitrate: int = sys.maxsize,
    ) -> None:
        self.url = url
        self.download_path = download_path
        self.max_bitrate = max_bitrate

    async def download(self) -> str:
        output_file_path = os.path.join(self.download_path, f'{uuid.uuid4()}.mp4')

        # Configure yt-dlp options
        ydl_opts = {
            'format': f'best[height<=1080][tbr<={self.max_bitrate//1000}]/best[height<=1080]',
            'outtmpl': output_file_path,
            'quiet': True,
            'no_warnings': True,
            "noprogress": True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://24ur.com/',
                'Origin': 'https://24ur.com',
            },
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            return output_file_path
        except yt_dlp_utils.DownloadError as e:
            raise exceptions.DownloadException(f'Download failed: {str(e)}')

    async def download_bytes(self) -> io.BytesIO:
        fp = await self.download()
        with open(fp, 'rb') as f:
            bytes_data = io.BytesIO(f.read())

        os.remove(fp)
        return bytes_data
