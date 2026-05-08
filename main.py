"""pygbag entry point - must live at project root."""

import asyncio

from app.game import Game


async def main() -> None:
    await Game().run()


asyncio.run(main())
