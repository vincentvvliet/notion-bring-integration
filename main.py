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
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["results"]


def get_shopping_items(page_id):
    blocks = get_children_blocks(page_id)
    items = []
    for block in blocks:
        if block["type"] == "bulleted_list_item":
            item = block['bulleted_list_item']['rich_text'][0]['plain_text']
            items.append(item)

    return items

if __name__ == "__main__":
    # Create Bring instance with email and password
    bring = Bring(BRING_EMAIL_ADDRESS, BRING_EMAIL_PASSWORD)
    bring.login()

    # Get information about all available shopping lists
    shopping_list = bring.loadLists()["lists"][2]

    items = get_shopping_items(BRING_SHOPPING_LIST)

    for item in items:
        item_info = item.split(', ')
        name = item_info[0]
        if len(item_info) == 2:
            specification = item_info[1]
            bring.saveItem(shopping_list['listUuid'], name, specification)
        else:
            bring.saveItem(shopping_list['listUuid'], name)


    # Get all the items of a list
    # items = bring.getItems(shopping_list['listUuid'])
    # todo_items = items["purchase"]
    # recent_items = items['recently']

    print("Successfully updated shopping list!")