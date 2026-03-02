import requests
import json # Import json to pretty print the output

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'dnt': '1',
    # Note: 'if-none-match' is an ETag for caching. For testing different dates,
    # you might want to remove it or update it if you get a 304 Not Modified.
    # For a fresh request, removing it is often best initially.
    # 'if-none-match': 'W/"2-l9Fw4VUO7kr8CvBlt4zaMCqXZ0w"',
    'origin': 'https://colorado-national-golf-club.book.teeitup.com',
    # 'priority': 'u=1, i', # This header is often set by the browser and may not be critical for programmatic requests.
    'referer': 'https://colorado-national-golf-club.book.teeitup.com/',
    # 'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"', # Browser-specific headers, usually not needed.
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"', # Browser-specific headers, usually not needed.
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    # 'x-be-alias': 'colorado-national-golf-club', # This might be important if the server uses it for routing. Keep it if issues arise.
}

# Define the date you want to query
target_date = '2026-02-27' # Example: Change to March 1st, 2026

params = {
    'localDate': target_date,
}

print(f"Attempting to fetch tee time locks for {target_date}...")

try:
    response = requests.get(
        'https://phx-api-be-east-1b.kenna.io/course/54f14bee0c8ad60378b019e3/tee-time/locks',
        params=params,
        headers=headers,
        timeout=10 # Add a timeout to prevent indefinite waiting
    )

    # Check for successful response
    response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")

    # Try to parse JSON response
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

