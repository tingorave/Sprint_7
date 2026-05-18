import allure
import pytest

from src.api.courier_api import CourierAPI
from src.data import messages


@allure.suite("Курьеры")
@allure.sub_suite("Удаление курьера")
class TestCourierDelete:
    @allure.title("Успешное удаление существующего курьера")
    @allure.description(
        "Создаём курьера через фикстуру, логинимся, получаем id и удаляем курьера. "
        "Ожидаем код 200 и тело {'ok': true}."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_courier_success(self, new_courier):
        with allure.step("Логинимся, чтобы получить id курьера"):
            login_response = CourierAPI.login_courier(
                {
                    "login": new_courier["login"],
                    "password": new_courier["password"],
                }
            )
            assert login_response.status_code == 200
            courier_id = login_response.json().get("id")
            assert courier_id is not None

        with allure.step("Удаляем курьера по его id"):
            delete_response = CourierAPI.delete_courier(courier_id)

        with allure.step("Проверяем код ответа и тело"):
            assert delete_response.status_code == 200
            body = delete_response.json()
            assert body.get("ok") is True

    @allure.title("Нельзя удалить курьера с несуществующим id")
    @allure.description(
        "Пробуем удалить курьера с несуществующим id. "
        "Ожидаем код 404 и сообщение 'Курьера с таким id нет'."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_courier_nonexistent_id(self):
        nonexistent_id = 99999999

        with allure.step("Пробуем удалить курьера с несуществующим id"):
            response = CourierAPI.delete_courier(nonexistent_id)

        with allure.step("Проверяем код ответа и сообщение об ошибке"):
            assert response.status_code == 404
            body = response.json()
            assert body["message"].startswith(messages.COURIER_DELETE_NOT_FOUND)