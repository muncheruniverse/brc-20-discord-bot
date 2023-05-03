# Munchers BRC20 Bot

A Python script that monitors the [Unisat Market](https://unisat.io/market) for new listings and sales of a specified token and sends a Discord webhook for each event.

## Requirements

This script requires Python 3 and the following Python packages:

- requests
- argparse

You can install these packages using `pip`. For example:

```
pip install requests argparse
```

## Usage

```
python main.py --ticker <ticker> --discord_webhook <discord_webhook_url>
```

where `<ticker>` is the BRC20 token symbol to monitor (e.g., `mnch`) and `<discord_webhook_url>` is the Discord webhook URL to send messages to.

Arguments:

```
  -h, --help            show this help message and exit
  --ticker TICKER, -t TICKER
                        BRC20 token symbol to monitor (default: mnch)
  --discord_webhook DISCORD_WEBHOOK, -d DISCORD_WEBHOOK
                        Discord webhook URL to send messages to
```

## Example

To monitor the `mnch` token and send messages to the Discord webhook at `https://discord.com/api/webhooks/1234567890`, run:

```
python main.py --ticker mnch --discord_webhook https://discord.com/api/webhooks/1234567890
```
