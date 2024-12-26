#!/usr/bin/env python

"""
SQLMapAPI: RESTful API for SQLMap
"""

from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# --- Tamper History Management ---
def load_tamper_history():
    if os.path.exists("tamper_history.json"):
        with open("tamper_history.json", "r") as f:
            return json.load(f)
    return {}

def save_tamper_history(history):
    with open("tamper_history.json", "w") as f:
        json.dump(history, f)

@app.route('/api/tamper-history', methods=['GET'])
def get_tamper_history():
    history = load_tamper_history()
    return jsonify({"status": "success", "data": history}), 200

@app.route('/api/tamper-history/reset', methods=['POST'])
def reset_tamper_history():
    save_tamper_history({})
    return jsonify({"status": "success", "message": "Tamper history reset successfully."}), 200

# --- Existing API Endpoints ---
@app.route('/version', methods=['GET'])
def version():
    return jsonify({"version": "1.5.7.7#dev", "success": True}), 200

@app.route('/task/new', methods=['GET'])
def new_task():
    return jsonify({"taskid": "fad44d6beef72285", "success": True}), 200

@app.route('/scan/<taskid>/start', methods=['POST'])
def start_scan(taskid):
    data = request.json
    return jsonify({"engineid": 19720, "success": True}), 200

@app.route('/scan/<taskid>/stop', methods=['GET'])
def stop_scan(taskid):
    return jsonify({"success": True}), 200

@app.route('/scan/<taskid>/status', methods=['GET'])
def scan_status(taskid):
    return jsonify({"status": "terminated", "returncode": 0, "success": True}), 200

@app.route('/scan/<taskid>/list', methods=['GET'])
def list_scan_options(taskid):
    return jsonify({"success": True, "options": []}), 200

@app.route('/scan/<taskid>/data', methods=['GET'])
def scan_data(taskid):
    return jsonify({"success": True, "data": [], "error": []}), 200

@app.route('/scan/<taskid>/log', methods=['GET'])
def scan_log(taskid):
    return jsonify({"success": True, "log": []}), 200

@app.route('/scan/<taskid>/kill', methods=['GET'])
def kill_scan(taskid):
    return jsonify({"success": True}), 200

@app.route('/task/<taskid>/delete', methods=['GET'])
def delete_task(taskid):
    return jsonify({"success": True}), 200

if __name__ == "__main__":
    app.run(port=8775)
