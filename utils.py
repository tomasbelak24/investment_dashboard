import requests
import os
import json
from datetime import datetime

def fetch_account_cash(api_key):
    url = "https://live.trading212.com/api/v0/equity/account/cash"
    headers = {"Authorization": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {
            "meta": {
                "type": "account_cash",
                "fetched_at": datetime.utcnow().isoformat() + "Z",
                "source_url": url
            },
            "data": data
        }
    except Exception as e:
        print(f"Error fetching account cash: {e}")
        return None

def save_json(data, type_name):
    os.makedirs("data", exist_ok=True)
    filepath = f"data/{type_name}.json"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def load_json(type_name):
    filepath = f"data/{type_name}.json"
    if os.path.exists(filepath):
        with open(filepath) as f:
            return json.load(f)
    return None
