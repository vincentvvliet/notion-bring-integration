import os
import requests
from dotenv import load_dotenv
from python_bring_api.bring import Bring

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
BRING_EMAIL_ADDRESS = os.getenv("BRING_EMAIL_ADDRESS")
BRING_EMAIL_PASSWORD = os.getenv("BRING_EMAIL_PASSWORD")
BRING_SHOPPING_LIST = os.getenv("BRING_SHOPPING_LIST")

# Headers for API requests
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def get_children_blocks(block_id):
    """ Retrieve all children of a given block id from Notion. """
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["results"]


def clear_page(block_id, children_ids):
    """ Clear given Notion page. """
    print("Clearing page...")
    for child_id in children_ids:
        url = f"https://api.notion.com/v1/blocks/{child_id}"
        response = requests.delete(url, headers=headers)
        response.raise_for_status()

    print("Successfully cleared the Notion page.")

def get_shopping_items(page_id, existing_items):
    """ Retrieve all shopping items from Bring API for a given page. Add only new items. """

    blocks = get_children_blocks(page_id)
    items = []
    block_ids = []
    for block in blocks:
        block_ids.append(block["id"])
        if block["type"] == "bulleted_list_item":
            item = block['bulleted_list_item']['rich_text'][0]['plain_text']
            if item.lower() not in existing_items:
                items.append(item)

    return items, block_ids


if __name__ == "__main__":
    # Create Bring instance with email and password
    bring = Bring(BRING_EMAIL_ADDRESS, BRING_EMAIL_PASSWORD)
    bring.login()

    # Get information about all available shopping lists
    shopping_list = bring.loadLists()["lists"][2]

    # Retrieve existing items from Bring
    existing_items = list(
        map(
            lambda x: f"{x['name']}{', ' + x['specification'] if x['specification'] != '' else ''}".lower(),
            bring.getItems(shopping_list['listUuid'])['purchase']
        )
    )

    # Retrieve new items from Notion
    new_items, block_ids = get_shopping_items(BRING_SHOPPING_LIST, existing_items)
    clear_page(BRING_SHOPPING_LIST, block_ids)

    if new_items:
        # Add new items to shopping list
        for item in new_items:
            item_info = item.split(', ')
            name = item_info[0]
            if len(item_info) == 2:
                specification = item_info[1]
                bring.saveItem(shopping_list['listUuid'], name, specification)
            else:
                bring.saveItem(shopping_list['listUuid'], name)

        print("Successfully updated shopping list!")

        # When all items have been added, clear notion page
        clear_page(BRING_SHOPPING_LIST, block_ids)
    else:
        print("No new items found!")
