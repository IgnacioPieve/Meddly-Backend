import requests

from config import WHATSAPP_API_KEY


def get_phone_numbers():
    whatsapp_business_account_id = 101547182706329
    user_access_token = WHATSAPP_API_KEY
    url = f'https://graph.facebook.com/v15.0/{whatsapp_business_account_id}/phone_numbers?access_token={user_access_token}'
    response = requests.get(url)
    print(response.text)


def register_phone():
    number_id = 100370432826961
    url = f'https://graph.facebook.com/v15.0/{number_id}/register'
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "messaging_product": "whatsapp",
        'pin': '100220'
    }
    result = requests.post(
        url,
        headers=headers,
        json=body,
    )
    print(result.text)


def send_message():
    message_data = [
        {
            "type": "text",
            "text": "Has agregado a Jorge como supervisor de tu cuenta"
        }
    ]
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "messaging_product": "whatsapp",
        "to": "+5493516637217",
        "type": "template",
        "template": {
            "name": 'generic_message',
            "language": {"code": "es"},
            "components": [
                {"type": "body", "parameters": message_data}
            ],
        },
    }
    result = requests.post(
        "https://graph.facebook.com/v15.0/100370432826961/messages",
        headers=headers,
        json=body,
    )

    print(result.text)


def request_verification_code():
    number_id = 100370432826961
    url = f'https://graph.facebook.com/v15.0/{number_id}/request_code?code_method=SMS&language=en_US&access_token={WHATSAPP_API_KEY}'
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
        "Content-Type": "application/json",
    }
    result = requests.post(
        url,
        headers=headers,
    )
    print(result.text)


def verificate_code():
    number_id = 100370432826961
    url = f'https://graph.facebook.com/v15.0/{number_id}/verify_code?code=788922&access_token={WHATSAPP_API_KEY}'
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
        "Content-Type": "application/json",
    }
    result = requests.post(
        url,
        headers=headers,
    )
    print(result.text)

send_message()
