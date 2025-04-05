import random
import string
import requests
import time

WEBHOOK_URL = "PUTYOURWEBHOOKHERE"
DISCORD_API_URL = "https://discordapp.com/api/v9/entitlements/gift-codes/{}?with_application=false&with_subscription_plan=true"

def generate_code(length=18):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def check_code(code):
    url = DISCORD_API_URL.format(code)
    response = requests.get(url)
    print(f"Checking code: {code} | Status: {response.status_code}")

    if response.status_code == 429:
        print("Uhh u got rate limited, gimme a second then ill continue")
        time.sleep(10)
        return False

    return response.status_code == 200

def send_to_webhook(code):
    payload = {"content": f"OMFG I FOUND A CODE I FOUND IT I FOUND IT https://discord.gift/{code}"}
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code in [200, 204]:
        print(f"CHECK THE SERVER")
    else:
        print(f"but ofc the webhook fucked up: {response.status_code} | {response.text}")

def main():
    while True:
        code = generate_code()
        if check_code(code):
            send_to_webhook(code)
        time.sleep(2)

if __name__ == "__main__":
    main()
