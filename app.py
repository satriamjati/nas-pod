from flask import Flask, request, jsonify
import subprocess
import os
from functools import wraps
from waitress import serve

app = Flask(__name__)

API_KEY = os.getenv("API_KEY", "default")

# Authentication decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if api_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route("/change-password", methods=["POST"])
@require_api_key
def change_password():
    data = request.get_json()
    username = data.get("username")
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not username or not old_password or not new_password:
        return jsonify({"error": "Missing parameters"}), 400

    # Step 1: Try authenticating using smbclient
    auth_command = [
        "smbclient",
        f"//localhost/{username}",
        "-U", f"{username}%{old_password}",
        "-c", "exit"
    ]

    auth_result = subprocess.run(auth_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if auth_result.returncode != 0:
        return jsonify({"error": "Authentication failed. Invalid old password."}), 403

    # Step 2: Run smbpasswd to change password
    change_command = f"echo -e '{new_password}\n{new_password}' | smbpasswd -s {username}"

    try:
        result = subprocess.run(change_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({"message": "Password changed successfully!"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Password change failed: {e.stderr.decode()}"}), 500

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
