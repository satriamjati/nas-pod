from flask import Flask, request, render_template, jsonify
import os
import requests
from waitress import serve

app = Flask(__name__)
API_KEY = os.getenv("API_KEY", "default")

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None

    if request.method == 'POST':
        username = request.form['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        retype_new_password = request.form['retype_new_password']

        if new_password != retype_new_password:
            message = "Error: New passwords do not match."
        else:
            url = "http://0.0.0.0:5000/change-password"
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": API_KEY
            }
            payload = {
                "username": username,
                "old_password": old_password,
                "new_password": new_password
            }

            try:
                response = requests.post(url, json=payload, headers=headers, timeout=5)
                if response.status_code == 200:
                    message = response.json().get("message", "No message returned.")
                else:
                    message = f"Error: {response.status_code} - {response.text}"
            except requests.exceptions.RequestException as e:
                message = f"Request failed: {str(e)}"

    return render_template('form.html', message=message)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
