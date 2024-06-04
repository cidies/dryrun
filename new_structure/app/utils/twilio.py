from twilio.rest import Client
import json

def make_call_route():
    config_path = 'c:\\temp\\config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)

    account_sid = config.get('twilio_account_sid')
    auth_token = config.get('twilio_auth_token')
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        twiml='<Response><Say>Ahoy, World!</Say></Response>',
        to=config.get('twilio_to'),
        from_=config.get('twilio_from')
    )

    print(call.sid)

def whatsapp_notification(title, description):
    config_path = 'c:\\temp\\config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)

    account_sid = config.get('twilio_account_sid')
    auth_token = config.get('twilio_auth_token')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f'{title}: {description}',
        to='whatsapp:+491743039038'
    )
