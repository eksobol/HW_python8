import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


class TestProducts:

    def test_product_check_quantity(self, product):
        assert product.check_quantity(100) is True
        assert product.check_quantity(0) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(215) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        product.buy(300)
        assert product.quantity == 700

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError, match="Запрашиваемое количество недоступно, только 1000 доступно для заказа."):
            product.buy(1001)


@pytest.fixture
def cart():
    return Cart()


class TestCart:

    def test_add_product_first(self, cart, product):
        cart.add_product(product, 1)
        assert product in cart.products
        assert cart.products[product] > 0

    def test_add_product(self, cart, product):
        cart.add_product(product, 10)
        cart.add_product(product, 20)
        cart.add_product(product, 5)
        assert cart.products[product] == 35

    def test_remove_product(self, cart, product):
        cart.add_product(product, 100)
        cart.add_product(product, 50)
        cart.add_product(product, 7)
        cart.remove_product(product, 60)
        assert cart.products[product] == 97

    def test_remove_product_all(self, cart, product):
        cart.add_product(product, 100)
        cart.add_product(product, 6)
        cart.remove_product(product)
        assert product not in cart.products

    def test_remove_product_max(self, cart, product):
        cart.add_product(product, 100)
        cart.add_product(product, 6)
        cart.remove_product(product, 200)
        assert product not in cart.products

    def test_clear(self, cart, product):
        cart.add_product(product, 100)
        cart.add_product(product, 80)
        cart.clear()
        assert product not in cart.products

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 80)
        assert cart.get_total_price() == 8000

    def test_buy_success(self, cart, product):
        cart.add_product(product, 80)
        assert product.quantity == 1000
        cart.buy()
        assert product.quantity == 920
        assert product not in cart.products

    def test_buy_fail(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError, match="Запрашиваемое количество товара недоступно"):
            cart.buy()

    def test_buy_empty(self, cart, product):
        cart.add_product(product, 10)
        cart.remove_product(product, )
        with pytest.raises(ValueError, match="В корзине нет товаров"):
            cart.buy()
