import requests

# The WhatsApp API key is stored in the config.py file
WHATSAPP_API_KEY = (
    "EAAIZAuL7Po9kBANjsVcKJIVwR9V6WTuwWyaMpW325sVotcnZCCzPvO2AP0SLzV"
    "FjZArsFjWFRpZAZC8EA8I29cOUcZC1h6C1EJjULlEGTwr9GZCuefgZBRbMJTvdt"
    "jjZBk41EdUt3rDfSvHKjFN4lHeZBadsnKAswRBV79mosZBaXBZCfOnc6Rii2ZAr"
    "DwacZB4yvKjdIY9Kke3r5darTzqaDhp1Na"
)
WA_BUSINESS_ACCOUNT_ID = 101547182706329  # ID of Meddly's WhatsApp Business Account

# ID of Meddly's WhatsApp number: +54 9 351 606-8857
# Can be obtained using the get_phone_numbers() function
NUMBER_ID = 100370432826961
PIN = "100220"

# Example data to send the message
EXAMPLE_MESSAGE = "Has agregado a Jorge como supervisor de tu cuenta"
EXAMPLE_RECEIVER = "+5493516637217"
EXAMPLE_TEMPLATE_NAME = "generic_message"


def get_phone_numbers():
    """
    Get a list of phone numbers associated with a WhatsApp Business Account.
    Docs: https://developers.facebook.com/docs/graph-api/reference/whats-app-business-account/phone_numbers
    """
    url = f"https://graph.facebook.com/v15.0/{WA_BUSINESS_ACCOUNT_ID}/phone_numbers?access_token={WHATSAPP_API_KEY}"
    return requests.get(url)


def register_phone():
    """
    Register a phone number to a WhatsApp Business Account.
    Docs: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/registration
    """
    url = f"https://graph.facebook.com/v15.0/{NUMBER_ID}/register"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {"messaging_product": "whatsapp", "pin": PIN}
    return requests.post(url, headers=headers, json=body)


def request_verification_code():
    """
    Use this edge to request a verification code for your phone number.
    Docs: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/phone-numbers
    """
    url = f"https://graph.facebook.com/v15.0/{NUMBER_ID}/request_code?code_method=SMS&language=en_US&access_token={WHATSAPP_API_KEY}"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
        "Content-Type": "application/json",
    }
    return requests.post(url, headers=headers)


def verificate_code():
    """
    Use this edge to verify your phone number.
    Docs: https://developers.facebook.com/docs/graph-api/reference/whats-app-business-account-to-number-current-status/verify_code/
    """
    url = f"https://graph.facebook.com/v15.0/{NUMBER_ID}/verify_code?code=788922&access_token={WHATSAPP_API_KEY}"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
        "Content-Type": "application/json",
    }
    return requests.post(url, headers=headers)


def send_message():
    """
    Send a message to a WhatsApp number.
    Docs: https://developers.facebook.com/docs/whatsapp/on-premises/reference/messages
    """
    url = f"https://graph.facebook.com/v15.0/{NUMBER_ID}/messages"
    message_data = [
        {"type": "text", "text": EXAMPLE_MESSAGE}
    ]
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "messaging_product": "whatsapp",
        "to": EXAMPLE_RECEIVER,
        "type": "template",
        "template": {
            "name": EXAMPLE_TEMPLATE_NAME,
            "language": {"code": "es"},
            "components": [{"type": "body", "parameters": message_data}],
        },
    }
    return requests.post(url, headers=headers, json=body)

# We can use the functions to send a message (i.e. send_message())
# send_message()

# Or, if we want to show the response, we can use the following code:
# print(send_message().text)
