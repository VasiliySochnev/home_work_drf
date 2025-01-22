import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course):
    """Создает продукт в страйпе"""

    return stripe.Product.create(name="course.title")


def create_stripe_price(price):
    """Создает цену в страйпе"""

    return stripe.Price.create(
        currency="rub",
        unit_amount=price * 100,
        product_data={"name": "course"},
    )


def create_stripe_session(price):
    """Создает сессию для получения ссылки на оплату."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
