from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

# Ganti dengan kredensial Vonage API Anda
VONAGE_API_KEY = 'c5a8dd17'
VONAGE_API_SECRET = 'RZYgoE91xyGjh23v'
VONAGE_WHATSAPP_NUMBER = '+14157386102'  # Nomor WhatsApp yang terdaftar di Vonage

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    to_number = data.get('to')
    message = data.get('text')
    
    if not to_number or not message:
        return jsonify({"error": "Invalid input"}), 400
    
    url = "https://messages-sandbox.nexmo.com/v1/messages"
    
    # Membuat header otorisasi Basic dengan base64 encoding
    auth_string = f"{VONAGE_API_KEY}:{VONAGE_API_SECRET}"
    b64_auth_string = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {b64_auth_string}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "from": VONAGE_WHATSAPP_NUMBER,
        "to": to_number,
        "message_type": "text",
        "text": message,
        "channel": "whatsapp"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        # Handle different types of exceptions
        return jsonify({"error": str(e)}), 500
    
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
