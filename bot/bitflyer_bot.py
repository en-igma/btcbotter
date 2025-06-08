import asyncio
import os
from typing import Optional

import pybotters


class BitflyerBot:
    """Sample bot skeleton for bitFlyer trading via pybotters."""

    def __init__(self, symbol: str = "BTC_JPY"):
        self.api_key = os.getenv("BITFLYER_API_KEY")
        self.api_secret = os.getenv("BITFLYER_API_SECRET")
        if not self.api_key or not self.api_secret:
            raise RuntimeError("API credentials are not set in environment variables")

        self.symbol = symbol
        self.client = pybotters.Client(
            apis={"bitflyer": {"key": self.api_key, "secret": self.api_secret}}
        )
        self.store = pybotters.bitflyer.DataStore()
        self.current_price: Optional[float] = None

    async def connect(self) -> None:
        """Connect websocket and start receiving ticker data."""
        await self.client.ws_connect(
            "wss://ws.lightstream.bitflyer.com/json-rpc",
            send_json={
                "method": "subscribe",
                "params": {"channel": f"lightning_ticker_{self.symbol}"},
            },
            hdlr=self.store.onmessage,
        )

    async def update_price(self) -> None:
        """Extract latest price from DataStore."""
        ticker = self.store.ticker.get("product_code", self.symbol)
        if ticker:
            self.current_price = ticker[-1]["ltp"]

    async def place_limit_order(self, side: str, price: float, size: float) -> str:
        """Place a limit order and return order ID."""
        order = {
            "product_code": self.symbol,
            "child_order_type": "LIMIT",
            "side": side,
            "price": price,
            "size": size,
        }
        resp = await self.client.post("/v1/me/sendchildorder", data=order)
        data = await resp.json()
        return data.get("child_order_acceptance_id")

    async def cancel_order(self, acceptance_id: str) -> None:
        params = {
            "product_code": self.symbol,
            "child_order_acceptance_id": acceptance_id,
        }
        await self.client.post("/v1/me/cancelchildorder", data=params)

    async def fetch_positions(self):
        """Return current positions."""
        resp = await self.client.get("/v1/me/getpositions", params={"product_code": self.symbol})
        return await resp.json()

    async def trading_logic(self):
        """Implement trading rules here."""
        pass

    async def run(self) -> None:
        async with self.client:
            await self.connect()
            while True:
                await self.update_price()
                await self.trading_logic()
                await asyncio.sleep(0.1)
