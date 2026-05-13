import requests

from .courier_api import BASE_URL


class OrdersAPI:
    @staticmethod
    def create_order(payload):
        return requests.post(f"{BASE_URL}/api/v1/orders", json=payload)

    @staticmethod
    def get_orders():
        return requests.get(f"{BASE_URL}/api/v1/orders")

    @staticmethod
    def accept_order(order_id, courier_id):
        params = {"courierId": courier_id}
        return requests.put(f"{BASE_URL}/api/v1/orders/accept/{order_id}", params=params)

    @staticmethod
    def get_order_by_track(track):
        params = {"t": track}
        return requests.get(f"{BASE_URL}/api/v1/orders/track", params=params)

    @staticmethod
    def cancel_order(track):
        params = {"track": track}
        return requests.put(f"{BASE_URL}/api/v1/orders/cancel", params=params)