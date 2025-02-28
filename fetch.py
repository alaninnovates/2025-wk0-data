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
    "https://frc-api.firstinspires.org/v3.0/2025/scores/WEEK0/qual",
    headers=headers,
    data=payload,
)
schedule = requests.request(
    "GET",
    "https://frc-api.firstinspires.org/v3.0/2025/schedule/WEEK0?tournamentLevel=qual",
    headers=headers,
    data=payload,
)
