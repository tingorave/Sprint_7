import allure
import pytest

from src.api.orders_api import OrdersAPI
from src.data import messages


def _create_order_and_get_track():
    payload = {
        "firstName": "Валентин",
        "lastName": "Миханоша",
        "address": "Москва, Тверская 1",
        "metroStation": "1",
        "phone": "+79990000000",
        "rentTime": 5,
        "deliveryDate": "2026-05-13",
        "comment": "Автотест: получить заказ по треку",
        "color": ["BLACK"],
    }
    response = OrdersAPI.create_order(payload)
    assert response.status_code == 201
    body = response.json()
    track = body.get("track")
    assert isinstance(track, int)
    return track


@allure.suite("Заказы")
@allure.sub_suite("Получение заказа по треку")
class TestOrdersGetByTrack:
    @allure.title("Успешное получение заказа по существующему треку")
    @allure.description(
        "Создаём заказ, получаем его track и запрашиваем заказ по этому треку. "
        "Ожидаем код 200 и корректную структуру тела ответа."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_order_by_valid_track(self):
        with allure.step("Создаём заказ и получаем его track"):
            track = _create_order_and_get_track()

        with allure.step("Запрашиваем заказ по этому треку"):
            response = OrdersAPI.get_order_by_track(track)

        with allure.step("Проверяем код ответа и структуру заказа"):
            assert response.status_code == 200
            body = response.json()
            order = body.get("order") or body
            assert isinstance(order, dict)
            assert order.get("track") == track

    @allure.title("Нельзя получить заказ по несуществующему треку")
    @allure.description(
        "Пробуем запросить заказ по несуществующему треку. "
        "Ожидаем код 404 и сообщение 'Заказ не найден'."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_order_by_nonexistent_track(self):
        nonexistent_track = 99999999

        with allure.step("Пробуем запросить заказ по несуществующему треку"):
            response = OrdersAPI.get_order_by_track(nonexistent_track)

        with allure.step("Проверяем код ответа и сообщение об ошибке"):
            assert response.status_code == 404
            body = response.json()
            assert body["message"] == messages.ORDER_NOT_FOUND

    @allure.title("Нельзя получить заказ без указания трека")
    @allure.description(
        "Отправляем запрос без параметра track. "
        "Ожидаем код 400 и сообщение 'Недостаточно данных для поиска'."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_order_without_track(self):
        with allure.step("Пробуем запросить заказ без трека"):
            response = OrdersAPI.get_order_by_track(None)

        with allure.step("Проверяем код ответа и сообщение об ошибке"):
            assert response.status_code == 400
            body = response.json()
            assert body["message"] == messages.ORDER_SEARCH_NOT_ENOUGH_DATA