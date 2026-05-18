import allure
import pytest

from src.api.courier_api import CourierAPI
from src.utils.generators import random_string
from src.data import messages


@allure.suite("Курьеры")
@allure.sub_suite("Создание курьера")
class TestCourierCreate:
    @allure.title("Успешное создание курьера с валидными данными")
    @allure.description(
        "Отправляем корректные login, password и firstName. "
        "Ожидаем код 201 и тело {'ok': true}."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_success(self):
        payload = {
            "login": random_string(),
            "password": random_string(),
            "firstName": "AutotestCourier",
        }

        with allure.step("Создаём курьера с валидными данными"):
            response = CourierAPI.create_courier(payload)

        with allure.step("Проверяем код ответа и тело"):
            assert response.status_code == 201
            body = response.json()
            assert body.get("ok") is True

    @allure.title("Нельзя создать двух курьеров с одинаковым логином")
    @allure.description(
        "Сначала создаём курьера, затем пробуем создать ещё одного с тем же login. "
        "Ожидаем код 409 и сообщение, что логин уже используется."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_duplicate_login(self):
        payload = {
            "login": "autotest_courier_duplicate",
            "password": "autotest_courier_password",
            "firstName": "AutotestCourier",
        }

        with allure.step("Создаём первого курьера"):
            first_response = CourierAPI.create_courier(payload)

        with allure.step("Пробуем создать второго курьера с тем же login"):
            second_response = CourierAPI.create_courier(payload)

        with allure.step("Проверяем, что первый запрос успешен или уже был дубль"):
            assert first_response.status_code in (201, 409)

        with allure.step("Проверяем, что второй запрос возвращает 409 и правильное сообщение"):
            assert second_response.status_code == 409
            body = second_response.json()
            assert body["message"].startswith(messages.COURIER_LOGIN_ALREADY_IN_USE)

    @allure.title("Нельзя создать курьера без логина")
    @allure.description(
        "Отправляем JSON без поля login. "
        "Ожидаем код 400 и сообщение 'Недостаточно данных для создания учетной записи'."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_without_login(self):
        payload = {
            # "login" отсутствует
            "password": "autotest_courier_password",
            "firstName": "AutotestCourier",
        }

        with allure.step("Пытаемся создать курьера без логина"):
            response = CourierAPI.create_courier(payload)

        with allure.step("Проверяем, что вернулся код 400 и сообщение об ошибке"):
            assert response.status_code == 400
            body = response.json()
            assert body["message"] == messages.COURIER_CREATE_NOT_ENOUGH_DATA

    @allure.title("Нельзя создать курьера без пароля")
    @allure.description(
        "Отправляем JSON без поля password. "
        "Ожидаем код 400 и сообщение 'Недостаточно данных для создания учетной записи'."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_without_password(self):
        payload = {
            "login": "autotest_courier_without_password",
            # "password" отсутствует
            "firstName": "AutotestCourier",
        }

        with allure.step("Пытаемся создать курьера без пароля"):
            response = CourierAPI.create_courier(payload)

        with allure.step("Проверяем, что вернулся код 400 и сообщение об ошибке"):
            assert response.status_code == 400
            body = response.json()
            assert body["message"] == messages.COURIER_CREATE_NOT_ENOUGH_DATA