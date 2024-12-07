import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "touch2023"
INSTAGRAM_ACCESS_TOKEN = "IGQWRPTDlBODJ3b1ZAPUWF4MkJPcXphdFVLc2hJa1NNaXdoalpBTEd0SEdaZAG95LVRTY05oUXRBNkFMRlhqcW56UDlQbVZAZAeVRvOE84NkYxNW1ndjlsSGZAsRXIwWC1XWDlfVWZAZALW9jNWotV2owR2pmTUhFVmxEMzAZD"
FLOWISE_WEBHOOK_URL = "https://touch.app.flowiseai.com/api/v1/prediction/3fbba34a-97d9-4ad9-902e-59557062c3f4"

def send_message_to_instagram(user_id, message_text):
    """Відправка відповіді назад в Instagram через API"""
    url = f"https://graph.facebook.com/v16.0/{user_id}/messages"
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": user_id},
        "message": {"text": message_text},
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"Response from Instagram API: {response.status_code}, {response.text}")

@app.route('/testhook', methods=['GET', 'POST'])
def testhook():
    if request.method == 'GET':
        # Верифікація вебхука
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("Webhook verified successfully.")
            return challenge, 200
        else:
            print("Verification failed.")
            return "Forbidden", 403

    elif request.method == 'POST':
        # Обробка POST-запитів
        print("POST Request Received")
        data = request.json
        print(f"JSON Data: {data}")

        # Перевіряємо повідомлення з Instagram
        if "entry" in data:
            for entry in data["entry"]:
                for messaging_event in entry.get("messaging", []):
                    if "message" in messaging_event:
                        sender_id = messaging_event["sender"]["id"]  # ID відправника
                        message_text = messaging_event["message"]["text"]  # Текст повідомлення

                        # Надсилаємо повідомлення до Flowise для обробки
                        flowise_payload = {"question": message_text}
                        try:
                            flowise_response = requests.post(
                                FLOWISE_WEBHOOK_URL, json=flowise_payload
                            )
                            flowise_output = flowise_response.json().get("output", "Не вдалося отримати відповідь.")
                            print(f"Flowise Response: {flowise_output}")

                            # Відправляємо згенеровану відповідь назад в Instagram
                            send_message_to_instagram(sender_id, flowise_output)
                        except Exception as e:
                            print(f"Error communicating with Flowise: {e}")

        return "EVENT_RECEIVED", 200

if __name__ == '__main__':
    app.run(port=5000)
