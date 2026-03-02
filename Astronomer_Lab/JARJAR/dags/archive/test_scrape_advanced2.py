import requests
import json

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'dnt': '1',
    # 'if-none-match': 'W/"a3d-Wv5P/6AZKJD4nKlBFzUOpQzFod8"', # Can remove for fresh requests
    'origin': 'https://colorado-national-golf-club.book.teeitup.com',
    # 'priority': 'u=1, i', # Browser-specific
    'referer': 'https://colorado-national-golf-club.book.teeitup.com/',
    # 'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"', # Browser-specific
    # 'sec-ch-ua-mobile': '?0', # Browser-specific
    # 'sec-ch-ua-platform': '"Windows"', # Browser-specific
    # 'sec-fetch-dest': 'empty', # Browser-specific
    # 'sec-fetch-mode': 'cors', # Browser-specific
    # 'sec-fetch-site': 'cross-site', # Browser-specific
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-be-alias': 'colorado-national-golf-club',
}

# Define the date and facility ID you want to query
target_date = '2026-02-28' # Use the date from the provided request
target_facility_ids = '1719' # Use the facility ID from the provided request

params = {
    'date': target_date,
    'facilityIds': target_facility_ids,
}

print(f"Attempting to fetch tee times for date: {target_date}, facility ID: {target_facility_ids}...")

try:
    response = requests.get(
        'https://phx-api-be-east-1b.kenna.io/v2/tee-times',
        params=params,
        headers=headers,
        timeout=15 # Increased timeout slightly due to the higher server response time
    )

    response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")

    try:
        data = response.json()
        print(f"Response Body (JSON): {json.dumps(data, indent=2)}")
    except json.JSONDecodeError:
        print("Response is not valid JSON.")
        print(f"Response Body (Raw): {response.text}")

except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print(f"Response Body (if available): {e.response.text}")
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: {e}")
except requests.exceptions.Timeout as e:
    print(f"Timeout Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"An unexpected error occurred: {e}")
