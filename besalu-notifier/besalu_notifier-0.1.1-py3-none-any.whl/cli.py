import json
import requests
import time
from notify_run import Notify
import logging
import datetime
import sys
import html
import click

logging.basicConfig(
    stream=sys.stdout, 
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)

logger = logging.getLogger(__name__)
notify = Notify()
url = "https://www.cafebesalu.com/app/store/api/v8/editor/users/125614995/sites/725420366501505624/store-locations/11e97377b326f4d1a5ad0cc47a2b63e4/products?page=1&per_page=200&has_categories=1"
# Default items to track
# watched_names = ['Ham & Swiss Pastry', 'Fruit Danish', 'Pain au Chocolat', 'Onion & Gruyere', 'Almond Croissant']

@click.group()
def cli():
    pass

@cli.command('list')
def list_items():        
    response = requests.get(url)
    data = response.json()['data']
    for item in data:
        short_desc = item['short_description'] or ''
        print(f"{item['name']}: {item['inventory']['total']}, {html.unescape(short_desc)}")

@cli.command()
@click.argument('items')
@click.option('--notify-ratio', default=1.0, help='What ratio of items need to be there to notify')
@click.option('--register/--no-register', ' /-r', default=True, help='Register a new Notify-Run channel?')
@click.option('--sleep', default=60, help='How long to wait (in seconds) between checks')
def watch(items, notify_ratio, register, sleep):
    if register:
        print("To get notificatins, follow these instructions:")
        print(notify.register())
    # items is a comma separated string, separate and clean up
    items_cleaned = [item.strip() for item in items.split(',')]
    while True:
        do_check(items_cleaned, notify_ratio)
        time.sleep(sleep)

# latch for only sending push notification when becomes true
last_success = False
def do_check(watched_items, notify_ratio):
    global last_success
    response = requests.get(url)
    data = response.json()['data']
    item_counts = {item['name']: item['inventory']['total'] for item in data}
    watched_item_counts = {key: value for key, value in item_counts.items() if key in watched_items}
    assert len(watched_item_counts) == len(watched_items)
    available_items = {key: value for key, value in watched_item_counts.items() if value > 0}
    available_ratio = len(available_items) / len(watched_items)
    if available_ratio >= notify_ratio:
        logger.info("Success! " + json.dumps(watched_item_counts))
        if not last_success:
            # Only notify once per latched becoming successful
            notify.send('Time to order besalu! ' + json.dumps(watched_item_counts))
        last_success = True
    else:
        logger.info("No dice. " + json.dumps(watched_item_counts))
        last_success = False

if __name__ == '__main__':
    cli()