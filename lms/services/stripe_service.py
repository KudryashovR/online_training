import stripe

from config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_product(name, description):
    """
    Создает новый продукт в Stripe.

    Аргументы:
    - name (str): Название продукта.
    - description (str): Описание продукта.

    Возвращает:
    - stripe.Product: Объект созданного продукта.
    """

    product = stripe.Product.create(
        name=name,
        description=description,
    )

    return product

def create_price(product_id, unit_amount, currency="usd"):
    """
    Создает новую цену для продукта в Stripe.

    Аргументы:
    - product_id (str): Идентификатор продукта.
    - unit_amount (int): Цена в минимальных единицах валюты (например, центы для USD).
    - currency (str): Код валюты (по умолчанию "usd").

    Возвращает:
    - stripe.Price: Объект созданной цены.
    """

    price = stripe.Price.create(
        product=product_id,
        unit_amount=unit_amount,
        currency=currency,
    )

    return price

def create_checkout_session(price_id, success_url, cancel_url):
    """
    Создает новую сессию Checkout в Stripe.

    Аргументы:
    - price_id (str): Идентификатор цены.
    - success_url (str): URL, на который будет перенаправлен пользователь при успешной оплате.
    - cancel_url (str): URL, на который будет перенаправлен пользователь при отмене оплаты.

    Возвращает:
    - stripe.checkout.Session: Объект созданной сессии Checkout.
    """

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )

    return session