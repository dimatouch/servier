from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Токени
VERIFY_TOKEN = "touch2023"
ACCESS_TOKEN = "EAB6PfZBaR3RUBO7E0wzfg70edSobbbgJRedjnHQ3zHLgfsmSXljkDqVZCTl1FTj5mEJmBMcCJ1m3ohH1hWMAZCZBktG8SPAUE3pzNR6vQMLGE9ugSFg8y62wNOFnkMj4grnZCy6y1nEn9JmDi5uD1dYrolurstZCNnb1bdnr2e9fID8vDRoKZCsZBM8BTExbacunIJ9KH0VTC7eKWPCjqK4VlJeHQ91wY2LPcTldJU6T"

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
        
        # Якщо приходить подія типу "messages"
        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for messaging_event in entry.get("messaging", []):
                    sender_id = messaging_event.get("sender", {}).get("id")  # ID користувача, який надіслав повідомлення
                    message = messaging_event.get("message", {}).get("text")  # Текст повідомлення

                    if sender_id and message:
                        print(f"Message from {sender_id}: {message}")
                        # Відправити відповідь користувачу
                        send_message(sender_id, f"Ви написали: {message}")
        return "EVENT_RECEIVED", 200

    else:
        return "Method Not Allowed", 405

def send_message(recipient_id, message_text):
    """
    Надсилає повідомлення користувачу в Instagram Direct.
    """
    url = f"https://graph.facebook.com/v16.0/me/messages?access_token={ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"Message sent to {recipient_id}: {message_text}")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")

if __name__ == '__main__':
    app.run(port=5000)
