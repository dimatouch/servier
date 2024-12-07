from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "touch2023"

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
        print(f"JSON Data: {request.json}")
        return jsonify({"message": "POST request received", "data": request.json}), 200

if __name__ == '__main__':
    app.run(port=5000)
