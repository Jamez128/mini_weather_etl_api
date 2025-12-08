import requests
import json
from pathlib import Path

# === CONFIG ===
BASE_URL = "https://api-open.data.gov.sg/v2/real-time/api/twenty-four-hr-forecast"
API_KEY = None
TIMEOUT = 5
OUTPUT_FILE = Path("provider_sample_response.json")

def fetch_provider_sample():
    headers = {}
    if API_KEY:
        headers["X-Api-Key"] = API_KEY

    try:
        print(f"Requesting: {BASE_URL}")
        resp = requests.get(BASE_URL, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()

        data = resp.json()

        # Pretty print to console
        print(json.dumps(data, indent=2))

        # Save to file
        OUTPUT_FILE.write_text(json.dumps(data, indent=2))
        print(f"\nSaved sample response to {OUTPUT_FILE}")

    except requests.exceptions.RequestException as exc:
        print(f"Request failed: {exc}")

if __name__ == "__main__":
    fetch_provider_sample()
