import requests
import json

url = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"
response = requests.get(url)

if response.status_code == 200:
    # Poora JSON data save kar rahe hain
    data = response.json(strict=False)
    with open("catalog.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print("Success! Data saved to catalog.json")
else:
    print(f"Error: {response.status_code}")