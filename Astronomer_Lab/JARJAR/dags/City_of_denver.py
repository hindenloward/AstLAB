import requests
from datetime import datetime, timedelta

API_URL = "https://api.membersports.com/api/v1/golfclubs/onlineBookingTeeTimes"
DAYS_AHEAD = 7

COURSES = [
    {"name": "Harvard Gulch Par 3", "golfClubId": 3713, "golfCourseId": 4781},
    {"name": "Kennedy (Creek 9 only)", "golfClubId": 3629, "golfCourseId": 20573},
    {"name": "Wellshire Back Nine", "golfClubId": 3831, "golfCourseId": 4928},
    {"name": "Kennedy Par 3 / Footgolf", "golfClubId": 3629, "golfCourseId": 4669},
    {"name": "City Park", "golfClubId": 3660, "golfCourseId": 4711},
    {"name": "Willis Case", "golfClubId": 3833, "golfCourseId": 4932},
]

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json; charset=UTF-8",
    "origin": "https://app.membersports.com",
    "referer": "https://app.membersports.com/",
    "user-agent": "Mozilla/5.0",
    "x-api-key": "A9814038-9E19-4683-B171-5A06B39147FC",
}

BASE_PAYLOAD = {
    "configurationTypeId": 1,
    "golfClubGroupId": 1,
    "groupSheetTypeId": 0,
}

def format_denver_time(value):
    value = int(value)
    hour = value // 100
    minute = value % 100

    if minute >= 60:
        hour += minute // 60
        minute %= 60

    return datetime(2000, 1, 1, hour, minute).strftime("%I:%M %p")


print("\nDENVER MUNICIPAL — ACTUALLY BOOKABLE TEE TIMES\n")

for course in COURSES:
    print(f"\n=== {course['name']} ===")

    for i in range(DAYS_AHEAD + 1):
        date = datetime.now() + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        readable_date = date.strftime("%A, %B %d %Y")

        print(f"\nDate: {readable_date}")
        print("-" * 60)

        payload = {
            **BASE_PAYLOAD,
            "date": date_str,
            "golfClubId": course["golfClubId"],
            "golfCourseId": course["golfCourseId"],
        }

        resp = requests.post(API_URL, headers=HEADERS, json=payload)
        if resp.status_code != 200:
            print("API error")
            continue

        tee_times = resp.json()
        printed_any = False

        for slot in tee_times:
            items = slot.get("items", [])
            if not items:
                continue

            # 🔑 TRUE BOOKABILITY CHECK
            bookable = any(
                i.get("bookingNotAllowed") is False
                and i.get("hide") is False
                for i in items
            )

            if not bookable:
                continue

            printed_any = True
            time_str = format_denver_time(slot["teeTime"])
            print(f"Tee Time: {time_str}")

        if not printed_any:
            print("No bookable tee times.")