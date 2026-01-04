import requests

BASE_URL = "http://localhost:5001"


def get_nearest_food_trucks(latitude=None, longitude=None, status=None):
    url = f"{BASE_URL}/api/MobileFoodTrucks/nearestFoodTrucks"
    headers = {"accept": "*/*"}
    params = {"latitude": latitude,
              "longitude": longitude,
              "status": status}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def search_food_trucks_by_street(street: str):
    url = f"{BASE_URL}/api/MobileFoodTrucks/searchByStreet"
    params = {"street": street}
    headers = {"accept": "*/*"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def search_food_trucks_by_name(name: str, status: str = None):
    url = f"{BASE_URL}/api/MobileFoodTrucks/searchByName"
    params = {"name": name}
    if status is not None:
        params["status"] = status
    headers = {"accept": "*/*"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()
