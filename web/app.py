from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

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
                "X-API-Key": "nomnom"
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
    app.run(debug=True, host='0.0.0.0', port=8080)
