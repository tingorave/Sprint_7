import requests
import allure

from src.config import API_PREFIX  # общий конфиг с базовым URL


class CourierAPI:
    @staticmethod
    @allure.step("Создание курьера")
    def create_courier(payload):
        return requests.post(f"{API_PREFIX}/courier", json=payload)

    @staticmethod
    @allure.step("Авторизация курьера")
    def login_courier(payload):
        return requests.post(f"{API_PREFIX}/courier/login", json=payload)

    @staticmethod
    @allure.step("Удаление курьера с id={courier_id}")
    def delete_courier(courier_id):
        return requests.delete(f"{API_PREFIX}/courier/{courier_id}")