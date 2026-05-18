import allure
import pytest

from src.api.courier_api import CourierAPI
from src.api.orders_api import OrdersAPI
from src.data import messages


def _create_order():
    """Вспомогательная функция для создания заказа и получения его track."""
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
        "Ожидаем код 200 и тело {'ok': true}."
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
            assert response.status_code == 200
            body = response.json()
            assert body.get("ok") is True

    @allure.title("Нельзя принять заказ с несуществующим id заказа")
    @allure.description(
        "Пробуем принять заказ с несуществующим id. "
        "Ожидаем код 404 и сообщение 'Заказа с таким id не существует'."
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
            assert response.status_code == 404
            body = response.json()
            assert body["message"] == messages.ORDER_ID_NOT_FOUND

    @allure.title("Нельзя принять заказ с несуществующим id курьера")
    @allure.description(
        "Создаём заказ и пробуем принять его с несуществующим id курьера. "
        "Ожидаем код 404 и сообщение 'Курьера с таким id не существует'."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_accept_order_nonexistent_courier_id(self):
        with allure.step("Создаём новый заказ и получаем его track"):
            track = _create_order()

        with allure.step("Получаем id заказа по его track"):
            order_id = _get_order_id_by_track(track)

        nonexistent_courier_id = 99999999

        with allure.step("Пробуем принять заказ с несуществующим id курьера"):
            response = OrdersAPI.accept_order(order_id, nonexistent_courier_id)

        with allure.step("Проверяем код ответа и сообщение об ошибке"):
            assert response.status_code == 404
            body = response.json()
            assert body["message"] == messages.COURIER_ID_NOT_FOUND

    @allure.title("Нельзя принять заказ без id курьера")
    @allure.description(
        "Создаём заказ и пробуем принять его без параметра courierId. "
        "Ожидаем код 400 и сообщение 'Недостаточно данных для поиска'."
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
            assert response.status_code == 400
            body = response.json()
            assert body["message"] == messages.ORDER_SEARCH_NOT_ENOUGH_DATA