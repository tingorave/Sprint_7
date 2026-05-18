import requests
import allure

from src.config import API_PREFIX  # общий модуль с базовым URL


class OrdersAPI:
    @staticmethod
    @allure.step("Создание заказа")
    def create_order(payload):
        return requests.post(f"{API_PREFIX}/orders", json=payload)

    @staticmethod
    @allure.step("Получение списка заказов")
    def get_orders():
        return requests.get(f"{API_PREFIX}/orders")

    @staticmethod
    @allure.step("Принятие заказа id={order_id} курьером id={courier_id}")
    def accept_order(order_id, courier_id):
        params = {"courierId": courier_id}
        return requests.put(f"{API_PREFIX}/orders/accept/{order_id}", params=params)

    @staticmethod
    @allure.step("Получение заказа по треку {track}")
    def get_order_by_track(track):
        params = {"t": track}
        return requests.get(f"{API_PREFIX}/orders/track", params=params)

    @staticmethod
    @allure.step("Отмена заказа с треком {track}")
    def cancel_order(track):
        params = {"track": track}
        return requests.put(f"{API_PREFIX}/orders/cancel", params=params)