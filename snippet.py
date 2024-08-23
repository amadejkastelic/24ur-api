import asyncio

from api_24ur import client


print(asyncio.run(client.get_post('https://www.24ur.com/novice/tujina/tisoci-spremljali-neposredni-prenos-rusitve-nekdanje-trumpove-igralnice.html')))