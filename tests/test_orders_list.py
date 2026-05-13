import allure

from src.api.orders_api import OrdersAPI


@allure.suite("Заказы")
@allure.sub_suite("Список заказов")
class TestOrdersList:
    @allure.title("Успешное получение списка заказов")
    @allure.description(
        "Отправляем запрос на получение списка заказов. "
        "Ожидаем код 200 и наличие массива заказов в теле ответа."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_orders_list_success(self):
        with allure.step("Отправляем запрос на получение списка заказов"):
            response = OrdersAPI.get_orders()

        with allure.step("Проверяем код ответа и структуру тела"):
            assert response.status_code == 200
            body = response.json()

            orders = (
                body.get("orders")
                or body.get("data")
                or body.get("items")
            )

            assert isinstance(orders, list)

            if orders:
                first = orders[0]
                assert isinstance(first, dict)
                assert (
                    "track" in first
                    or "id" in first
                )