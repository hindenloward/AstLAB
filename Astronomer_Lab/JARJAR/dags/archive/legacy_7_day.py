import requests
import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+

BASE_API = "https://cityofwestminster.cps.golf/onlineres/onlineapi/api/v1/onlinereservation"
SEARCH_PAGE = "https://cityofwestminster.cps.golf/onlineresweb/search-teetime"

DAYS_AHEAD = 7

print("\nCITY OF WESTMINSTER (CPS) TEE TIMES:\n")

session = requests.Session()

# Step 1 — Initialize session (creates V4COOKIE)
session.get(SEARCH_PAGE)

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

for i in range(DAYS_AHEAD + 1):

    target_date = datetime.now() + timedelta(days=i)
    formatted_date = target_date.strftime("%a %b %d %Y")
    readable_date = target_date.strftime("%Y-%m-%d (%A)")

    print(f"\nDate: {readable_date}")
    print("-" * 60)

    # Step 2 — Generate fresh transaction ID
    transaction_id = str(uuid.uuid4())

    headers = base_headers.copy()
    headers["x-requestid"] = str(uuid.uuid4())

    # Step 3 — Register transaction ID
    register_response = session.post(
        f"{BASE_API}/RegisterTransactionId",
        headers=headers,
        json={"transactionId": transaction_id},
    )

    if register_response.status_code != 200:
        print("Failed to register transaction:", register_response.text)
        continue

    # Step 4 — Call TeeTimes using SAME transaction ID
    params = {
        "searchDate": formatted_date,
        "holes": "0",
        "numberOfPlayer": "0",
        "courseIds": "1",
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

    response = session.get(
        f"{BASE_API}/TeeTimes",
        headers=headers,
        params=params,
    )

    if response.status_code != 200:
        print("Error fetching tee times:", response.text)
        continue

    data = response.json()

    content = data.get("content")

    if not content or not isinstance(content, list):
        print("No tee times available.")
        continue

    for tee in data["content"]:

        # Convert time to Mountain Time
        utc_time = datetime.fromisoformat(tee["startTime"])
        local_time = utc_time.replace(tzinfo=ZoneInfo("UTC")).astimezone(
            ZoneInfo("America/Denver")
        )
        time_str = local_time.strftime("%I:%M %p")

        # Available spots
        available_spots = len(tee.get("availableParticipantNo", []))

        # Pricing extraction
        green_fee = 0
        cart_fee = 0

        for item in tee.get("shItemPrices", []):
            if "GreenFee" in item.get("shItemCode", ""):
                green_fee = float(item.get("price", 0))
            if "Cart" in item.get("shItemCode", ""):
                cart_fee = float(item.get("price", 0))

        walking_price = green_fee
        riding_price = green_fee + cart_fee

        print(
            f"Tee Time: {time_str} "
            f"— Available Spots: {available_spots} "
            f"— Holes: {tee.get('holes')} "
            f"— Walking: ${walking_price:.2f} "
            f"— Cart: ${riding_price:.2f}"
        )