import pytest
import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru"


def _random_string(length=10):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))


@pytest.fixture
def new_courier():
    courier = {
        "login": _random_string(),
        "password": _random_string(),
        "firstName": _random_string(),
    }
    response = requests.post(f"{BASE_URL}/api/v1/courier", json=courier)
    assert response.status_code == 201
    yield courier
    login_resp = requests.post(
        f"{BASE_URL}/api/v1/courier/login",
        json={
            "login": courier["login"],
            "password": courier["password"],
        },
    )
    if login_resp.status_code == 200:
        courier_id = login_resp.json().get("id")
        if courier_id:
            requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")