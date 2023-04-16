import datetime
import os
import requests

NUTRITIONIX_ID = os.environ["NUTRITIONIX_ID"]
NUTRITIONIX_API_KEY = os.environ["NUTRITIONIX_API_KEY"]
sheety_authorization = os.environ["SHEETY_AUTH"]

headers = {
    "x-app-id": f"{NUTRITIONIX_ID}",
    "x-app-key": f"{NUTRITIONIX_API_KEY}",
}

sheety_headers = {
    "Authorization": f"{sheety_authorization}"
}
parameters = {
    "age": "23",
    "gender": "female",
    "weight_kg": f"{45}",
    "query": f"{input('Tell me what exercises you did: ')}"
}


def nutritionix_exercises(request_headers, request_body):
    """Provide json values that correspond to the header and the request_body"""
    nutritionix_response = requests.post(url="https://trackapi.nutritionix.com/v2/natural/exercise",
                                         headers=request_headers,
                                         json=request_body)
    data = nutritionix_response.json()["exercises"]
    return data


def current_date_time():
    """Returns a tuple of current day and time converted to strings."""
    date = datetime.datetime.today().date().strftime("%d/%m/%Y")
    time = datetime.datetime.today().time().strftime("%H:%M:%S")
    return date, time


current_date, current_time = current_date_time()
exercises = nutritionix_exercises(request_headers=headers, request_body=parameters)

for exercise in exercises:
    exercise_name = exercise["name"]
    duration = exercise["duration_min"]
    calories = exercise["nf_calories"]
    sheety_parameters = {
        "workout":
            {
                "date": current_date,
                "time": current_time,
                "exercise": exercise_name,
                "duration": duration,
                "calories": calories
            }
    }
    sheety_response = requests.post(url="https://api.sheety.co/username/projectName/sheetName", # API Example not a valid one.
                                    headers=sheety_headers, json=sheety_parameters)
