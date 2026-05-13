import allure
import pytest

from src.api.orders_api import OrdersAPI


def get_base_order_payload():
    return {
        "firstName": "Валентин",
        "lastName": "Миханоша",
        "address": "Москва, Тверская 1",
        "metroStation": "1",
        "phone": "+79990000000",
        "rentTime": 5,
        "deliveryDate": "2026-05-13",
        "comment": "Автотест заказа",
    }


@allure.suite("Заказы")
@allure.sub_suite("Создание заказа")
class TestOrdersCreate:
    @allure.title("Успешное создание заказа с разными вариантами цвета")
    @allure.description(
        "Отправляем запрос создания заказа с разными вариантами поля color: "
        "один цвет, второй цвет, оба цвета, без цвета. "
        "Ожидаем код 201 и наличие track в ответе."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "colors",
        [
            pytest.param(["BLACK"], id="color_black"),
            pytest.param(["GREY"], id="color_grey"),
            pytest.param(["BLACK", "GREY"], id="color_black_and_grey"),
            pytest.param([], id="color_empty"),
        ],
    )
    def test_create_order_with_different_colors(self, colors):
        payload = get_base_order_payload()
        payload["color"] = colors

        with allure.step(f"Создаём заказ с цветами: {colors}"):
            response = OrdersAPI.create_order(payload)

        with allure.step("Проверяем код ответа и наличие track"):
            assert response.status_code == 201
            body = response.json()
            assert "track" in body
            assert isinstance(body["track"], int)