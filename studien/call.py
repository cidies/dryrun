# Filename: make_call.py
# python call.py "+491743039038" "You've been hacked!"

import sys, json
from twilio.rest import Client

def make_call(to_number, message):
    # Load the config file
    config_path = 'c:\\temp\\config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)

    account_sid = config.get('twilio_account_sid')
    auth_token = config.get('twilio_auth_token')

    client = Client(account_sid, auth_token)

    call = client.calls.create(
        twiml=f'<Response><Say>{message}</Say></Response>',
        to=to_number,
        from_='+13343782044'
    )

    print(call.sid)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python make_call.py <to_number> <message>")
        sys.exit(1)

    to_number = sys.argv[1]
    message = sys.argv[2]

    make_call(to_number, message)