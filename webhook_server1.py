from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/testhook', methods=['GET', 'POST'])
def testhook():
    if request.method == 'GET':
        # Логування GET-запитів
        print("GET Request Received")
        print(f"Query Params: {request.args}")
        return jsonify({"message": "GET request received", "params": request.args}), 200

    elif request.method == 'POST':
        # Логування POST-запитів
        print("POST Request Received")
        print(f"JSON Data: {request.json}")
        return jsonify({"message": "POST request received", "data": request.json}), 200

if __name__ == '__main__':
    app.run(port=5000)