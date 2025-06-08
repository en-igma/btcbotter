# btcbotter

Sample Bitcoin auto-trading bot using [pybotters](https://github.com/pybotters/pybotters).

This project provides a skeleton for connecting to bitFlyer via WebSocket,
placing and cancelling limit orders and querying positions. Implement your
trading rules in `BitflyerBot.trading_logic`.

## Requirements

- Python 3.11 or later
- pybotters

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Environment Variables

Set your bitFlyer API key and secret before running:

```bash
export BITFLYER_API_KEY="your_api_key"
export BITFLYER_API_SECRET="your_api_secret"
```

## Usage

Run the bot:

```bash
python main.py
```

The bot subscribes to ticker updates via WebSocket and includes skeleton
methods for order management and position handling.
