import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from waitress import serve
from azure.communication.email import EmailClient

load_dotenv()
app = Flask(__name__)

connection_string = os.environ.get("CONNECTION_STRING")
client = EmailClient.from_connection_string(connection_string)
sender = os.environ.get("SENDER_ADDRESS")

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()

    if 'email' not in data or 'subject' not in data or 'body' not in data:
        return jsonify({'error': 'Missing required fields'})

    try:

        message = {
            "senderAddress": os.environ.get("SENDER_ADDRESS"),
            "recipients":  {
                "to": [{"address": data['email']}],
            },
            "content": {
                "subject": data['subject'],
                "plainText": data['asunto'],
            }
        }

        poller = client.begin_send(message)
        result = poller.result()

    except Exception as ex:
        print(ex)
    return jsonify(data)


if __name__ == '__main__':
    print('server running')
    serve(app, host='0.0.0.0', port=5000)
