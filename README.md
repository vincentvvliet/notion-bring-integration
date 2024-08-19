# Notion Bring Integration
This project is dedicated to connecting [Notion](https://www.notion.so/) and [Bring](https://www.getbring.com/en/home). By specifying the given shopping list `page_id` from Notion in the `.env`, this program will simply add all (non-duplicate) items from the given page to Bring. The reason for this is that I find it easier to type out a list in notion than to add seperate items in Bring. 

## Prerequisites
- Items in the shopping list page must be represented in a `bulleted list`.
- Specifications can be added to an item in the form: `item_name, item_specification`. These specifications will be taken into account in Bring.

## Environment Variables
Create a `.env` file containing the following information:
- `BRING_EMAIL_ADDRESS` = Email address used in Bring
- `BRING_EMAIL_PASSWORD` = Password used in Bring
- `BRING_SHOPPING_LIST` = Shopping list id
- `NOTION_API_KEY` = Notion API key

## Tools
This project was done in python and requires API keys from:
- [python-bring-api library](https://pypi.org/project/python-bring-api/)
- [Bring API](https://www.getbring.com/en/integration-check)
- [Notion API](https://developers.notion.com/)
