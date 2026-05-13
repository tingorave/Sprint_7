import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru"


class CourierAPI:
    @staticmethod
    def create_courier(payload):
        return requests.post(f"{BASE_URL}/api/v1/courier", json=payload)

    @staticmethod
    def login_courier(payload):
        return requests.post(f"{BASE_URL}/api/v1/courier/login", json=payload)

    @staticmethod
    def delete_courier(courier_id):
        return requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")