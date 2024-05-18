from flask import Flask, render_template, request, jsonify
from threading import Timer
import json
import os

app = Flask(__name__)

DATA_DIR = 'data'

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), 'r') as file:
        return json.load(file)

def save_json(filename, data):
    with open(os.path.join(DATA_DIR, filename), 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def dashboard():
    notifications = load_json('notifications.json')
    exercises = load_json('exercises.json')
    return render_template('dashboard.html', notifications=notifications, exercises=exercises)

@app.route('/scenarios')
def scenarios():
    scenarios = load_json('scenarios.json')
    return render_template('scenarios.html', scenarios=scenarios)

@app.route('/communication')
def communication():
    return render_template('communication.html')

@app.route('/reports')
def reports():
    reports = load_json('reports.json')
    return render_template('reports.html', reports=reports)

@app.route('/injects')
def injects():
    injects = load_json('injects.json')
    return render_template('injects.html', injects=injects)

@app.route('/schedule_exercise', methods=['POST'])
def schedule_exercise():
    data = request.json
    injects = load_json('injects.json')
    exercise_injects = [inject for inject in injects if inject['title'] in data['inject_titles']]

    if data['type'] == 'timed':
        for idx, inject in enumerate(exercise_injects):
            delay = idx * data['interval'] * 60  # convert minutes to seconds
            Timer(delay, execute_inject, [inject]).start()
    elif data['type'] == 'manual':
        save_json('scheduled_injects.json', exercise_injects)

    return jsonify({"status": "scheduled"}), 200

@app.route('/execute_inject/<inject_title>')
def execute_inject_route(inject_title):
    injects = load_json('scheduled_injects.json')
    inject = next((inject for inject in injects if inject['title'] == inject_title), None)
    if inject:
        execute_inject(inject)
    return jsonify({"status": "executed"}), 200

def execute_inject(inject):
    # Simulate sending inject via the specified communication type
    print(f"Executing inject: {inject['title']} via {inject['communication_type']}")
    # In real implementation, send email, text, call, or personal notification here

@app.route('/api/notifications', methods=['GET', 'POST'])
def api_notifications():
    if request.method == 'GET':
        return jsonify(load_json('notifications.json'))
    elif request.method == 'POST':
        data = request.json
        save_json('notifications.json', data)
        return jsonify({"status": "success"}), 200

@app.route('/api/exercises', methods=['GET', 'POST'])
def api_exercises():
    if request.method == 'GET':
        return jsonify(load_json('exercises.json'))
    elif request.method == 'POST':
        data = request.json
        save_json('exercises.json', data)
        return jsonify({"status": "success"}), 200

@app.route('/api/scenarios', methods=['GET', 'POST'])
def api_scenarios():
    if request.method == 'GET'):
        return jsonify(load_json('scenarios.json'))
    elif request.method == 'POST':
        data = request.json
        save_json('scenarios.json', data)
        return jsonify({"status": "success"}), 200

@app.route('/api/reports', methods=['GET', 'POST'])
def api_reports():
    if request.method == 'GET':
        return jsonify(load_json('reports.json'))
    elif request.method == 'POST'):
        data = request.json
        save_json('reports.json', data)
        return jsonify({"status": "success"}), 200

@app.route('/api/injects', methods=['GET', 'POST'])
def api_injects():
    if request.method == 'GET':
        return jsonify(load_json('injects.json'))
    elif request.method == 'POST':
        data = request.json
        save_json('injects.json', data)
        return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)