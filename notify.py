# app/modules/notify.py
import os
def send_whatsapp(message_body, to_numbers=None):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_whatsapp = os.getenv("TWILIO_WHATSAPP_NUMBER")
    technicians = os.getenv("TECHNICIAN_WHATSAPP_NUMBER", "")
    if not all([account_sid, auth_token, from_whatsapp]):
        return False
    try:
        from twilio.rest import Client
        client = Client(account_sid, auth_token)
        targets = to_numbers or [n.strip() for n in technicians.split(",") if n.strip()]
        for t in targets:
            to = t if t.startswith("whatsapp:") else f"whatsapp:{t}"
            client.messages.create(body=message_body, from_=from_whatsapp, to=to)
        return True
    except Exception as e:
        print(f"Erro send_whatsapp: {e}")
        return False
