import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+

# --- Config ---
BASE_URL = "https://phx-api-be-east-1b.kenna.io/v2/tee-times"
FACILITY_ID = "13099"  # Stoney Creek
DAYS_AHEAD = 7

headers = {
    'accept': 'application/json, text/plain, */*',
    'origin': 'https://stoney-creek-golf-course.book.teeitup.golf',
    'referer': 'https://stoney-creek-golf-course.book.teeitup.golf/',
    'user-agent': 'Mozilla/5.0',
    'x-be-alias': 'stoney-creek-golf-course',
}



for i in range(DAYS_AHEAD + 1):
    target_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
    print("\nSTONEY CREEK GOLF COURSE:\n")
    params = {
        "date": target_date,
        "facilityIds": FACILITY_ID
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()

        date_obj = datetime.strptime(target_date, "%Y-%m-%d")
        day_name = date_obj.strftime("%A")

        print(f"Date: {target_date} ({day_name})")
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
            # --- Convert UTC tee time to local time ---
            raw_time = tee.get("teetime")
            if raw_time:
                utc_time = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
                local_time = utc_time.astimezone(ZoneInfo("America/Denver"))
                time_str = local_time.strftime("%I:%M %p")
            else:
                time_str = "N/A"

            # --- Remaining spots ---
            booked_players = tee.get("bookedPlayers", 0)
            MAX_TEE_CAPACITY = 4
            available_spots = max(0, MAX_TEE_CAPACITY - booked_players)

            # --- Rate info ---
            # --- Rate info ---
            rates = tee.get("rates", [])
            price = "N/A"
            holes = "N/A"

            rates = tee.get("rates", [])
            if rates:
                rate = rates[0]
                holes = rate.get("holes", "N/A")
                green_fee_cart = rate.get("dueOnlineWalking", 0)
                if green_fee_cart == 0:
                    green_fee_waking = rate.get("greenFeeWalking", 0)
                    transaction_fee = rate.get("transactionFees", 0)
                    price = f"${(green_fee_waking / 100 + transaction_fee):.2f}"
                else:
                    transaction_fee = rate.get("transactionFees", 0)
                    price = f"${(green_fee_cart / 100 + transaction_fee):.2f}"
            else:
                holes = "N/A"
                price = "N/A"
            print(
                f"Tee Time: {time_str} — Available spots: {available_spots} "
                f"— Holes: {holes} — Price: {price}"
            )

        print("\n")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {target_date}: {e}\n")