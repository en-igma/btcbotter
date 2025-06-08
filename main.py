import asyncio

from bot.bitflyer_bot import BitflyerBot


def main() -> None:
    bot = BitflyerBot()
    asyncio.run(bot.run())


if __name__ == "__main__":
    main()
