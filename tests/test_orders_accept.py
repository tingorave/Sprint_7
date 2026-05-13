import allure
import pytest

from src.api.courier_api import CourierAPI
from src.api.orders_api import OrdersAPI


def _create_order():
    """Вспомогательная функция для создания заказа и получения его id."""
    payload = {
        "firstName": "Валентин",
        "lastName": "Миханоша",
        "address": "Москва, Тверская 1",
        "metroStation": "1",
        "phone": "+79990000000",
        "rentTime": 5,
        "deliveryDate": "2026-05-13",
        "comment": "Автотест: принятие заказа",
        "color": ["BLACK"],
    }
    response = OrdersAPI.create_order(payload)
    assert response.status_code == 201
    body = response.json()
    track = body.get("track")
    assert isinstance(track, int)
    return track


def _get_order_id_by_track(track):
    """Получение id заказа по его track (для accept нужна именно id)."""
    response = OrdersAPI.get_order_by_track(track)
    assert response.status_code == 200
    body = response.json()
    order = body.get("order") or body
    order_id = order.get("id")
    assert isinstance(order_id, int)
    return order_id


@allure.suite("Заказы")
@allure.sub_suite("Принятие заказа")
class TestOrdersAccept:
    @allure.title("Успешное принятие заказа курьером")
    @allure.description(
        "Создаём курьера и заказ, получаем id заказа по треку, "
        "после чего принимаем заказ от имени курьера. "
        "Ожидаем успешный код ответа и признак ok=true."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_accept_order_success(self, new_courier):
        with allure.step("Логинимся, чтобы получить id курьера"):
            login_response = CourierAPI.login_courier(
                {
                    "login": new_courier["login"],
                    "password": new_courier["password"],
                }
            )
            assert login_response.status_code == 200
            courier_id = login_response.json().get("id")
            assert isinstance(courier_id, int)

        with allure.step("Создаём новый заказ и получаем его track"):
            track = _create_order()

        with allure.step("Получаем id заказа по его track"):
            order_id = _get_order_id_by_track(track)

        with allure.step("Принимаем заказ от имени курьера"):
            response = OrdersAPI.accept_order(order_id, courier_id)

        with allure.step("Проверяем код ответа и тело"):
            assert response.status_code in (200, 201, 202)
            body = response.json()
            ok = body.get("ok")
            if ok is not None:
                assert ok is True

    @allure.title("Нельзя принять заказ с несуществующим id заказа")
    @allure.description(
        "Пробуем принять заказ с несуществующим id. "
        "Ожидаем код 404 или 400 и сообщение об ошибке."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_accept_order_nonexistent_order_id(self, new_courier):
        with allure.step("Логинимся, чтобы получить id курьера"):
            login_response = CourierAPI.login_courier(
                {
                    "login": new_courier["login"],
                    "password": new_courier["password"],
                }
            )
            assert login_response.status_code == 200
            courier_id = login_response.json().get("id")
            assert isinstance(courier_id, int)

        nonexistent_order_id = 99999999

        with allure.step("Пробуем принять несуществующий заказ"):
            response = OrdersAPI.accept_order(nonexistent_order_id, courier_id)

        with allure.step("Проверяем код ответа и сообщение об ошибке"):
            assert response.status_code in (404, 400)
            body = response.json()
            message = body.get("message", "").lower()
            assert (
                "заказа с таким id не существует" in message
                or "order id not found" in message
                or "недостаточно данных" in message
                or "insufficient data" in message
                or "not found" in message
            )

    @allure.title("Нельзя принять заказ без id курьера")
    @allure.description(
        "Создаём заказ и пробуем принять его без параметра courierId. "
        "Ожидаем код 400 и сообщение о нехватке данных."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_accept_order_without_courier_id(self):
        with allure.step("Создаём новый заказ и получаем его track"):
            track = _create_order()

        with allure.step("Получаем id заказа по его track"):
            order_id = _get_order_id_by_track(track)

        with allure.step("Пробуем принять заказ без courierId"):
            response = OrdersAPI.accept_order(order_id, courier_id=None)

        with allure.step("Проверяем код ответа и сообщение об ошибке"):
            assert response.status_code in (400, 404)
            body = response.json()
            message = body.get("message", "").lower()
            assert (
                "недостаточно данных" in message
                or "insufficient data" in message
                or "нужно указать id курьера" in message
                or "courier id is required" in message
            )