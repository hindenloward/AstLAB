import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+

# --- Config ---
BASE_URL = "https://phx-api-be-east-1b.kenna.io/v2/tee-times"
FACILITY_ID = "1719"
DAYS_AHEAD = 7

headers = {
    'accept': 'application/json, text/plain, */*',
    'origin': 'https://colorado-national-golf-club.book.teeitup.com',
    'referer': 'https://colorado-national-golf-club.book.teeitup.com/',
    'user-agent': 'Mozilla/5.0',
    'x-be-alias': 'colorado-national-golf-club',
}

print("\nCOLORADO NATIONAL, ERIE:\n")

for i in range(DAYS_AHEAD + 1):  # today + next 7 days
    target_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")

    params = {
        "date": target_date,
        "facilityIds": FACILITY_ID
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()

        print(f"Date: {target_date}")
        print("-" * 50)

        if not data:
            print("No data returned.\n")
            continue

        day_data = data[0]
        tee_times = day_data.get("teetimes", [])

        if not tee_times:
            print("No tee times available.\n")
            continue

        for tee in tee_times:

            # --- Convert UTC tee time to Mountain Time ---
            raw_time = tee.get("teetime")
            if raw_time:
                utc_time = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
                local_time = utc_time.astimezone(ZoneInfo("America/Denver"))
                time_str = local_time.strftime("%I:%M %p")
            else:
                time_str = "N/A"

            # --- Calculate available players ---
            # --- Calculate true remaining spots ---
            booked_players = tee.get("bookedPlayers", 0)

            # Colorado National max group size is 4
            MAX_TEE_CAPACITY = 4

            available_spots = MAX_TEE_CAPACITY - booked_players

            # Prevent negatives just in case
            if available_spots < 0:
                available_spots = 0

            players_display = available_spots
            # --- Extract rate info ---
            rates = tee.get("rates", [])
            if rates:
                rate = rates[0]
                holes = rate.get("holes", "N/A")

                green_fee_cart = rate.get("greenFeeCart", 0)
                price = f"${green_fee_cart / 100:.2f}"
            else:
                holes = "N/A"
                price = "N/A"

            print(
                f"Tee Time: {time_str} — Available spots: {players_display} "
                f"— Holes: {holes} — Price: {price}"
            )

        print("\n")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {target_date}: {e}\n")