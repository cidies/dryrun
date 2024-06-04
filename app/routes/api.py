from flask import Blueprint, request, jsonify
from app.utils.json_utils import load_json, save_json

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/notifications', methods=['GET', 'POST'])
def api_notifications():
    if request.method == 'GET':
        return jsonify(load_json('notifications.json'))
    elif request.method == 'POST':
        data = request.json
        save_json('notifications.json', data)
        return jsonify({"status": "success"}), 200

@api_bp.route('/api/exercises', methods=['GET', 'POST'])
def api_exercises():
    if request.method == 'GET':
        return jsonify(load_json('exercises.json'))
    elif request.method == 'POST':
        data = request.json
        save_json('exercises.json', data)
        return jsonify({"status": "success"}), 200

@api_bp.route('/api/scenarios', methods=['GET', 'POST'])
def api_scenarios():
    if request.method == 'GET':
        return jsonify(load_json('scenarios.json'))
    elif request.method == 'POST':
        data = request.json
        save_json('scenarios.json', data)
        return jsonify({"status": "success"}), 200

@api_bp.route('/api/reports', methods=['GET', 'POST'])
def api_reports():
    if request.method == 'GET':
        return jsonify(load_json('reports.json'))
    elif request.method == 'POST':
        data = request.json
        save_json('reports.json', data)
        return jsonify({"status": "success"}), 200

@api_bp.route('/api/injects', methods=['GET', 'POST'])
def api_injects():
    if request.method == 'GET':
        return jsonify(load_json('injects.json'))
    elif request.method == 'POST':
        data = request.json
        save_json('injects.json', data)
        return jsonify({"status": "success"}), 200
