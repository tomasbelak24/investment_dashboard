import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

api_key = os.getenv("API_KEY_212")
print(api_key)

url = "https://live.trading212.com/api/v0/equity/account/cash"

headers = {"Authorization": api_key}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    
    structured_data = {
        "meta": {
            "type": "account_cash",
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "source_url": url
        },
        "data": data
    }

    # Ensure 'data' folder exists
    os.makedirs("data", exist_ok=True)

    # Save to file
    with open("data/account_cash.json", "w") as f:
        json.dump(structured_data, f, indent=4)

    print("✅ Data saved to data/account_cash.json")

else:
    print(f"❌ Failed to fetch data. Status code: {response.status_code}")