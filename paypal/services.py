import base64
import requests

from django.conf import settings


def get_access_token():
    """
    Obtiene un OAuth Token desde PayPal Sandbox.
    """

    auth = base64.b64encode(
        f"{settings.PAYPAL_CLIENT_ID}:{settings.PAYPAL_SECRET}".encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        f"{settings.PAYPAL_API}/v1/oauth2/token",
        headers=headers,
        data={
            "grant_type": "client_credentials"
        },
    )

    response.raise_for_status()

    data = response.json()

    return data["access_token"]

def create_order(invoice):

    token = get_access_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    body = {

        "intent": "CAPTURE",

        "purchase_units": [

            {

                "reference_id": str(invoice.id),

                "amount": {

                    "currency_code": "USD",

                    "value": str(invoice.total)

                }

            }

        ]

    }

    response = requests.post(

        f"{settings.PAYPAL_API}/v2/checkout/orders",

        headers=headers,

        json=body

    )

    response.raise_for_status()

    return response.json()

def capture_order(order_id):

    token = get_access_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(

        f"{settings.PAYPAL_API}/v2/checkout/orders/{order_id}/capture",

        headers=headers,

    )

    response.raise_for_status()

    return response.json()