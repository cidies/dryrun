# Add notification related functions here


def textnote(title, description):
    # Load the config file
    config_path = 'c:\\temp\\config.json'
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logging.error(f"[textnote] Config file not found at {config_path}")
        return
    except json.JSONDecodeError:
        logging.error(f"[textnote] Failed to parse JSON from config file at {config_path}")
        return

    # Define the Slack API URL and headers
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {config.get('text_token_keys')}",
        "Content-type": "application/json"
    }
    print(f"[**********] Bearer {config.get('text_token_keys')}")
    # Define the data to send
    data = {
        "channel": "alerts",
        "text": f"{title}: {description}"
    }

def threema_message(title, description):
    # Load the config file
    config_path = 'c:\\temp\\config.json'
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logging.error(f"[threema_message] Config file not found at {config_path}")
        return
    except json.JSONDecodeError:
        logging.error(f"[threema_message] Failed to parse JSON from config file at {config_path}")
        return

    # Define the Threema Gateway API URL and headers
    url = "https://msgapi.threema.ch/send_simple"
    headers = {
        "Content-type": "application/json"
    }

    # Define the data to send
    data = {
        "from": config.get('threema_from'),
        "to": config.get('threema_to'),
        "text": f"{title}: {description}"
    }

    # Send the request
    response = requests.post(url, headers=headers, data=json.dumps(data), auth=(config.get('threema_api_identity'), config.get('threema_api_secret')))

    # Check the response
    if response.status_code != 200:
        logging.error(f"[threema_message] Failed to send message: {response.content}") 

    # Send the request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        logging.info(f"[textnote] Sent Slack notification with title: {title} and description: {description}")
    except requests.exceptions.RequestException as e:
        logging.error(f"[textnote] Failed to send Slack notification. RequestException: {e}")
    except Exception as e:
        logging.error(f"[textnote] Failed to send Slack notification with title: {title} and description: {description}. Error: {e}")




def whatsapp_notification(title, description):
        # Load the config file
    config_path = 'c:\\temp\\config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)

    account_sid = config.get('twilio_account_sid')
    auth_token = config.get('twilio_auth_token')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='{title}: {description}',
    #to='whatsapp:+491726719759'
    to='whatsapp:+491743039038'
)

