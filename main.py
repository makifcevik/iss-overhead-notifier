import requests
import smtplib
import time
from datetime import datetime

LAT = 41.066285
LNG = 28.946157
USER = "user"
PASSWORD = "password"

parameters = {
    "iss_lat": LAT,
    "iss_lng": LNG,
    "formatted": 0
}


def is_iss_overhead():
    iss_response = requests.get("http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()
    iss_lat = float(iss_data["iss_position"]["iss_latitude"])
    iss_lng = float(iss_data["iss_position"]["longitude"])
    if LAT-5 <= iss_lat <= LAT+5 and LNG-5 <= iss_lng <= LNG+5:
        return True


def is_night():
    sun_response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()
    sun_data = sun_response.json()
    sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    if time_now > sunset or time_now < sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=USER, password=PASSWORD)
        connection.sendmail(from_addr=USER, to_addrs=USER, msg="Subject: LOOK UP!\n\n Maybe you can see something!")
