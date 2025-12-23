import webview
from flask import Flask, send_from_directory, request, jsonify
import threading
import os
import sys
from logic.database import Database
from logic.economy import EconomyManager
from logic.api import GameAPI

# 1. Setup Flask to serve UI and API
app = Flask(__name__, static_folder='ui')
global_api = None # Placeholder for our logic

@app.route('/')
def serve_index():
    return send_from_directory('ui', 'index.html')

@app.route('/<path:path>')
def serve_assets(path):
    return send_from_directory('ui', path)

# --- WEB API ROUTES (For Browser Users) ---
@app.route('/api/login', methods=['POST'], strict_slashes=False)
def web_login():
    data = request.json or {}
    result = global_api.login(data.get('username'), data.get('password'))
    return jsonify(result)

@app.route('/api/signup', methods=['POST'], strict_slashes=False)
def web_signup():
    data = request.json or {}
    result = global_api.signup(data.get('username'), data.get('password'))
    return jsonify(result)

@app.route('/api/sync', methods=['GET'], strict_slashes=False)
def web_sync():
    result = global_api.get_sync_data()
    # Return empty success if no user logged in yet to avoid browser errors
    if result is None:
        return jsonify({"status": "waiting"})
    return jsonify(result)

@app.route('/api/roll', methods=['POST'], strict_slashes=False)
def web_roll():
    result = global_api.roll_item()
    return jsonify(result)

def run_flask():
    # Fixed port 5000 for consistency
    app.run(port=5000, debug=False, use_reloader=False)

def main():
    global global_api

    # 2. Initialize Logic
    db = Database()
    economy = EconomyManager(db)
    global_api = GameAPI(economy, db)

    # 3. Start Flask in a background thread
    server_thread = threading.Thread(target=run_flask, daemon=True)
    server_thread.start()

    # 4. Launch the Window
    print("Launching Engine at http://127.0.0.1:5000")
    window = webview.create_window(
        title='AURA FORGE: BRAINROT EDITION',
        url='http://127.0.0.1:5000',
        js_api=global_api,
        width=1000,
        height=700
    )

    webview.start(debug=True)
    economy.running = False

if __name__ == '__main__':
    main()
