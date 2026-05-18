import pytest
import requests

from src.utils.generators import random_string
from src.config import API_PREFIX  # общий базовый URL для API


@pytest.fixture
def new_courier():
    courier = {
        "login": random_string(),
        "password": random_string(),
        "firstName": random_string(),
    }

    response = requests.post(f"{API_PREFIX}/courier", json=courier)
    assert response.status_code == 201

    yield courier

    login_resp = requests.post(
        f"{API_PREFIX}/courier/login",
        json={
            "login": courier["login"],
            "password": courier["password"],
        },
    )
    if login_resp.status_code == 200:
        courier_id = login_resp.json().get("id")
        if courier_id:
            requests.delete(f"{API_PREFIX}/courier/{courier_id}")