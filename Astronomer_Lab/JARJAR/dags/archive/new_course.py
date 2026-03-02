import requests
import uuid
from datetime import datetime

BASE_URL = "https://cityofwestminster.cps.golf/onlineres/onlineapi/api/v1/onlinereservation"

session = requests.Session()

# Step 1 — load search page (get V4COOKIE)
session.get("https://cityofwestminster.cps.golf/onlineresweb/search-teetime")

headers = {
    "accept": "application/json, text/plain, */*",
    "client-id": "onlineresweb",
    "origin": "https://cityofwestminster.cps.golf",
    "referer": "https://cityofwestminster.cps.golf/onlineresweb/search-teetime",
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

# Step 2 — generate a UUID
transaction_id = str(uuid.uuid4())

headers["x-requestid"] = str(uuid.uuid4())

# Step 3 — REGISTER the transaction
register_response = session.post(
    f"{BASE_URL}/RegisterTransactionId",
    headers=headers,
    json={"transactionId": transaction_id}
)

print("Register:", register_response.status_code, register_response.text)

# Step 4 — now call TeeTimes using SAME transaction_id
params = {
    "searchDate": datetime.now().strftime("%a %b %d %Y"),
    "holes": "0",
    "numberOfPlayer": "0",
    "courseIds": "1,4,2",
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
    f"{BASE_URL}/TeeTimes",
    headers=headers,
    params=params
)

print("TeeTimes:", response.status_code)
print(response.text)