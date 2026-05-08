"""Entry point."""

import asyncio

from app.game import Game


async def main() -> None:
    await Game().run()


asyncio.run(main())
