import requests
import json
import time
import argparse

# Define the command line arguments
parser = argparse.ArgumentParser(description='Monitor the Unisat market and send Discord notifications for new listings and sales')
parser.add_argument('--ticker', type=str, help='the ticker of the token to monitor', required=True)
parser.add_argument('--discord_webhook', type=str, help='the Discord webhook URL to send notifications to', required=True)
args = parser.parse_args()

# Set up the initial state
prev_listings = []

# Define the URL and payload
url = 'https://unisat.io/unisat-market-v2/auction/actions'
payload = {
    "filter": {"tick": args.ticker},
    "start": 0,
    "limit": 5
}

# Define a function to send the Discord webhook
def send_discord_webhook(listings, event):
    # Create the Discord message
    message = {
        "channel_id": "CHANNEL_ID",
        "content": "",
        "tts": False,
        "embeds": [
            {
                "type": "rich",
                "title": "New Sales 🚀" if event == "Sold" else "New Listings 👹",
                "description": "",
                "color": 0x9ecf61 if event == "Sold" else 0x619acf,
                "fields": [],
                "footer": {
                    "text": "@muncherverse brc-20 Bot 🤖"                    
                },
                "url": f"https://unisat.io/market?tick={args.ticker}&tab=2"
            }
        ]
    }

    # Add the listings to the message
    for listing in listings:
        unit_price = listing['unitPrice']
        amount = listing['amount']
        price = listing['price']
        name = listing['name']
        field_name = f"{amount:,} ${name}"
        field_value = f"{price:,} sats ({unit_price:,} sats/${name})"
        message['embeds'][0]['fields'].append({
            "name": field_name,
            "value": field_value,
            "inline": False
        })
    data = {
        "content": "",
        "embeds": message['embeds']
    }

    # Send the webhook
    requests.post(args.discord_webhook, json=data)

# Loop forever
while True:
    # Make the request
    response = requests.post(url, json=payload)
    
    # Parse the response
    data = json.loads(response.text)['data']
    new_listings = data['list']
    
    # Check for new listings
    new_sold_listings = []
    new_listed_listings = []
    for listing in new_listings:
        if listing not in prev_listings:
            if listing['event'] == 'Sold':
                new_sold_listings.append(listing)
            elif listing['event'] == 'Listed':
                new_listed_listings.append(listing)
    
    # Send the Discord webhooks for new listings
    if len(new_sold_listings) > 0:
        send_discord_webhook(new_sold_listings, 'Sold')
    if len(new_listed_listings) > 0:
        send_discord_webhook(new_listed_listings, 'Listed')
    
    # Update the previous listings
    prev_listings = new_listings
    
    # Wait for a minute before making the next request
    time.sleep(60)
