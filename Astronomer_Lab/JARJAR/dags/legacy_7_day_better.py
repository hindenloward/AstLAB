import requests
import uuid
from datetime import datetime, timedelta

# CPS API endpoints
BASE_API = "https://cityofwestminster.cps.golf/onlineres/onlineapi/api/v1/onlinereservation"
SEARCH_PAGE = "https://cityofwestminster.cps.golf/onlineresweb/search-teetime"

# Number of days ahead to check
DAYS_AHEAD = 7

# Courses mapping
COURSES = {
    1: "Legacy Ridge",
    2: "Walnut Creek"
}

# Initialize session to get V4COOKIE
session = requests.Session()
session.get(SEARCH_PAGE)

# Base headers (shared)
base_headers = {
    "accept": "application/json, text/plain, */*",
    "client-id": "onlineresweb",
    "origin": "https://cityofwestminster.cps.golf",
    "referer": SEARCH_PAGE,
    "user-agent": "Mozilla/5.0",
    "x-apikey": "8ea2914e-cac2-48a7-a3e5-e0f41350bf3a",
    "x-componentid": "1",
    "x-ismobile": "false",
    "x-moduleid": "7",
    "x-productid": "1",
    "x-siteid": "2",
    "x-terminalid": "3",
    "x-timezone-offset": "420",
    "x-timezoneid": "America/Denver",
    "x-websiteid": "be7f2728-0758-4a72-fe80-08d97849167d",
}

print("\nCITY OF WESTMINSTER 7-DAY TEE TIMES\n")

for course_id, course_name in COURSES.items():
    

    for i in range(DAYS_AHEAD + 1):
        target_date = datetime.now() + timedelta(days=i)
        formatted_date = target_date.strftime("%a %b %d %Y")
        readable_date = target_date.strftime("%Y-%m-%d (%A)")
        print(f"\n--- {course_name} ---\n")
        print(f"Date: {readable_date}")
        print("-" * 60)

        # Generate fresh transaction and request IDs
        transaction_id = str(uuid.uuid4())
        headers = base_headers.copy()
        headers["x-requestid"] = str(uuid.uuid4())

        # Register transaction
        register_resp = session.post(
            f"{BASE_API}/RegisterTransactionId",
            headers=headers,
            json={"transactionId": transaction_id}
        )
        if register_resp.status_code != 200:
            print("Failed to register transaction:", register_resp.text)
            continue

        # Request tee times
        params = {
            "searchDate": formatted_date,
            "holes": "0",  # 0 = all, 9 = only 9-hole, 18 = only 18-hole
            "numberOfPlayer": "0",  # 0 = any
            "courseIds": str(course_id),
            "searchTimeType": "0",
            "transactionId": transaction_id,
            "teeOffTimeMin": "0",
            "teeOffTimeMax": "23",
            "isChangeTeeOffTime": "true",
            "teeSheetSearchView": "5",
            "classCode": "R",
            "defaultOnlineRate": "N",
            "isUseCapacityPricing": "false",
            "memberStoreId": "1",
            "searchType": "1",
        }

        headers["x-requestid"] = str(uuid.uuid4())
        resp = session.get(f"{BASE_API}/TeeTimes", headers=headers, params=params)

        if resp.status_code != 200:
            print("Error fetching tee times:", resp.text)
            continue

        data = resp.json()
        content = data.get("content")

        # Handle no tee times
        if not content or not isinstance(content, list):
            print("No tee times available.\n")
            continue

        for tee in content:
            if not isinstance(tee, dict):
                continue

            # Tee time (already in Mountain Time)
            local_time = datetime.fromisoformat(tee["startTime"])
            time_str = local_time.strftime("%I:%M %p")

            # Available spots
            available_spots = len(tee.get("availableParticipantNo", []))

            # Pricing
            green_fee = 0
            cart_fee = 0
            for item in tee.get("shItemPrices", []):
                if "GreenFee" in item.get("shItemCode", ""):
                    green_fee = float(item.get("price", 0))
                if "Cart" in item.get("shItemCode", ""):
                    cart_fee = float(item.get("price", 0))

            walking_price = green_fee
            riding_price = green_fee + cart_fee

            holes = tee.get("holes", "N/A")

            print(
                f"Tee Time: {time_str} "
                f"— Available Spots: {available_spots} "
                f"— Holes: {holes} "
                f"— Walking: ${walking_price:.2f} "
                f"— With Cart: ${riding_price:.2f}"
            )
        print("\n")