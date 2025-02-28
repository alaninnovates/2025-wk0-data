import requests
import base64

auth = "Basic " + base64.b64encode(
    b"alaninnovates:d8e2444e-1670-4920-a4aa-268b929810dc"
).decode("utf-8")

payload = {}
headers = {
    "If-Modified-Since": "",
    "Authorization": auth,
}

matches = requests.request(
    "GET",
    "https://frc-api.firstinspires.org/v3.0/2025/scores/ISDE1/qual",
    headers=headers,
    data=payload,
)
schedule = requests.request(
    "GET",
    "https://frc-api.firstinspires.org/v3.0/2025/schedule/ISDE1?tournamentLevel=qual",
    headers=headers,
    data=payload,
)

import json

matches = json.loads(matches.text)
schedule = json.loads(schedule.text)

with open("matches.json", "w") as f:
    json.dump(matches, f)

with open("schedules.json", "w") as f:
    json.dump(schedule, f)
