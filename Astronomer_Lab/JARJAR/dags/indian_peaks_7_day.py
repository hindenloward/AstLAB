import requests
import uuid
from datetime import datetime, timedelta

BASE_API = "https://indianpeaks.cps.golf/onlineres/onlineapi/api/v1/onlinereservation"
SEARCH_PAGE = "https://indianpeaks.cps.golf/onlineresweb/search-teetime"

DAYS_AHEAD = 7

COURSES = {
    10: "Indian Peaks 18",
    11: "Indian Peaks 9",
}

session = requests.Session()
session.get(SEARCH_PAGE)  # sets V4COOKIE

base_headers = {
    "accept": "application/json, text/plain, */*",
    "client-id": "onlineresweb",
    "origin": "https://indianpeaks.cps.golf",
    "referer": SEARCH_PAGE,
    "user-agent": "Mozilla/5.0",
    "x-apikey": "8ea2914e-cac2-48a7-a3e5-e0f41350bf3a",
    "x-componentid": "1",
    "x-ismobile": "false",
    "x-moduleid": "7",
    "x-productid": "1",
    "x-siteid": "1",
    "x-terminalid": "3",
    "x-timezone-offset": "420",
    "x-timezoneid": "America/Denver",
    "x-websiteid": "f04abbc1-368f-40f4-096d-08d89aea9574",
}

print("\nINDIAN PEAKS 7-DAY TEE TIMES\n")

for course_id, course_name in COURSES.items():
    

    for i in range(DAYS_AHEAD + 1):
        target_date = datetime.now() + timedelta(days=i)

        formatted_date = target_date.strftime("%a %b %d %Y")
        readable_date = target_date.strftime("%Y-%m-%d (%A)")
        print(f"\n=== {course_name} ===")
        print(f"\nDate: {readable_date}")
        print("-" * 60)

        transaction_id = str(uuid.uuid4())
        headers = base_headers.copy()
        headers["x-requestid"] = str(uuid.uuid4())

        # Register transaction
        reg = session.post(
            f"{BASE_API}/RegisterTransactionId",
            headers=headers,
            json={"transactionId": transaction_id}
        )

        if reg.status_code != 200:
            print("Transaction registration failed")
            continue

        params = {
            "searchDate": formatted_date,
            "holes": "0",
            "numberOfPlayer": "0",
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
        resp = session.get(
            f"{BASE_API}/TeeTimes",
            headers=headers,
            params=params
        )

        if resp.status_code != 200:
            print("Error fetching tee times")
            continue

        data = resp.json()
        content = data.get("content")

        # Handle CPS inconsistencies
        if isinstance(content, dict):
            content = content.get("teeTimeList", [])
        elif isinstance(content, str):
            import json
            content = json.loads(content)
        elif not isinstance(content, list):
            content = []

        if not content:
            print("No tee times available.")
            continue

        for tee in content:
            start = datetime.fromisoformat(tee["startTime"])
            time_str = start.strftime("%I:%M %p")

            spots = len(tee.get("availableParticipantNo", []))
            holes = tee.get("holes", "N/A")

            green_fee = 0
            cart_fee = 0

            for item in tee.get("shItemPrices", []):
                code = item.get("shItemCode", "")
                price = float(item.get("price", 0))
                if "GreenFee" in code:
                    green_fee = price
                elif "Cart" in code:
                    cart_fee = price

            print(
                f"Tee Time: {time_str} "
                f"— Spots: {spots} "
                f"— Holes: {holes} "
                f"— Walking: ${green_fee:.2f} "
                f"— With Cart: ${green_fee + cart_fee:.2f}"
            )