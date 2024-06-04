import time
import logging
from flask_socketio import SocketIO
from threading import Timer
from app.utils.json_utils import load_json, save_json
from datetime import datetime

socketio = SocketIO()

def load_exercise(id):
    exercises = load_json('exercises.json')
    for exercise in exercises:
        if exercise['id'] == int(id):
            return exercise
    return None

def perform_exercise(exercise):
    socketio.emit('message', {'data': 'Execution started!'})

    if exercise is None:
        socketio.emit('message', {'data': 'Error: exercise not found'})
        return False

    exercises = load_json('exercises.json')
    injects = load_json('injects.json')

    if 'inject_order' not in exercise:
        socketio.emit('message', {'data': 'Error: No inject_order in exercise'})
        return False

    for inject_id in exercise['inject_order']:
        inject = next((inject for inject in injects if inject['id'] == inject_id), None)
        if inject is None:
            continue

        title = inject.get('title', 'No title')
        duration = inject.get('duration', 10)
        communication_type = inject.get('communication_type')
        
        for i in range(5, 0, -1):
            socketio.emit('message', {'data': f'Countdown: {i}'})
            time.sleep(1)
        
        socketio.emit('message', {'data': f'Inject {inject_id} wird ausgeführt: {title} für {duration} Sekunden per {communication_type}'})

        if communication_type:
            if communication_type == 'text':
                textnote(f"[{exercise.get('name', 'No title')}] {inject.get('title', 'No title')}", inject.get('nachrichtentext', 'No description'))

            elif communication_type == 'email':
                email(f"[{exercise.get('name', 'No title')}] {inject.get('title', 'No title')}", inject.get('nachrichtentext', 'No description'))

        time.sleep(duration)

    exercise['last_performed'] = datetime.now().isoformat()
    for i, ex in enumerate(exercises):
        if ex['id'] == exercise['id']:
            exercises[i] = exercise
            break

    save_json('exercises.json', exercises)
    socketio.emit('message', {'data': 'Scenario updated successfully'})

    return True
