# Noch zu tun:
# Siehe github issues

# Die Injects können über verschiedene Wege kommuniziert werden.
# Im Moment nur auf der executed_exercise.html Seite
# Ich muss das noch implementieren, dass die Injects auch
# über Email, SMS oder Telefon kommuniziert werden können
# Dazu brauche ich dann auch die entsprechenden Felder
# in den Injekten und auch die Funktionen, die die Kommunikation
# durchführen




from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from threading import Timer
import json
import os
from flask_toastr import Toastr
from flask import flash, get_flashed_messages
import time
from flask_socketio import SocketIO
from threading import Thread
import logging


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
toastr = Toastr(app)
socketio = SocketIO(app)

DATA_DIR = 'data'

logging.basicConfig(level=logging.INFO)

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

@app.route('/injects', endpoint='injects')
def injects_route():
    injects_data = load_json('injects.json')
    return render_template('injects.html', injects=injects_data)

def get_inject_by_id(inject_id):
    injects_data = load_json('injects.json')
    for inject in injects_data:
        if inject['id'] == inject_id:
            return inject
    return None

@app.template_filter('id_to_name')
def id_to_name(id):
    scenarios = load_json('scenarios.json')  # Laden Sie die Szenarien aus der JSON-Datei
    scenario = next((s for s in scenarios if s['id'] == str(id)), None)
    if scenario is not None:
        return scenario['name']
    else:
        return 'Unbekanntes Szenario'


#### E X E R C I S E S ####

@app.route('/update_exercise/<id>', methods=['POST'])
def update_exercise(id):
    # Load the exercises from the JSON file
    exercises = load_json('exercises.json')

    # Find the exercise with the given ID
    for exercise in exercises:
        if exercise['id'] == int(id):
            # Update the exercise with the form data
            exercise['name'] = request.form['name']
            exercise['description'] = request.form['description']
            exercise['target_team'] = request.form['target_team']
            exercise['last_performed'] = request.form['last_performed']
            # Add more lines here to update other exercise properties

            # Save the exercises back to the JSON file
            save_json('exercises.json', exercises)

            # Show a toast message
            flash('Exercise updated successfully')
            print('[*] Flashed message:', 'Exercise updated successfully')

            # Return a response
            return redirect(url_for('exercises'))

    # If no exercise with the given ID was found, return an error
    flash('Exercise not found')
    #return redirect(url_for('dashboard'))
    return redirect(url_for('exercises'))


@app.route('/schedule_exercise_form')
def schedule_exercise_form():
    return render_template('exercise_planung.html')

@app.route('/exercises')
def exercises():
    exercises = load_json('exercises.json')  # Load the exercises from the JSON file
    print(exercises)  # Print the exercises data
    return render_template('exercises.html', exercises=exercises)  # Pass the exercises to the template


def load_exercise(id):
    exercises = load_json('exercises.json')  # Load the exercises from the JSON file
    for exercise in exercises:
        if exercise['id'] == int(id):  # Convert the ID to an integer before comparing
            return exercise
    return None

@app.route('/edit_exercise/<id>')
def edit_exercise(id):
    exercise = load_exercise(id)
    if exercise is not None:
        return render_template('edit_exercise.html', exercise=exercise)
    else:
        return "Exercise not found", 404
    
@socketio.on('start_exercise')
def perform_exercise(exercise):
    time.sleep(10)
    print("[PE.01] perform_exercise called")
    socketio.emit('message', {'data': 'Execution started!'})

    if exercise is None:
        print("[*] Error: exercise cannot be None")
        socketio.emit('message', {'data': 'Error: exercise not found'})
        return False

    print("[PE.02] Loading exercises from exercises.json")
    exercises = load_json('exercises.json')

    print("[PE.03] Loading injects from injects.json")
    injects = load_json('injects.json')

    # Print the exercises and injects for debugging
    #print(f"[*] Loaded exercises: {exercises}")
    #print(f"[*] Loaded injects: {injects}")

    if not 'inject_order' in exercise:
        print("[*] No inject_order in exercise")
        socketio.emit('message', {'data': 'Error: No inject_order in exercise'})
        return False

    print("[PE.04] Running through injects in the order specified in the exercise")
    for inject_id in exercise['inject_order']:
        print(f"[PE.05] Looking for inject with ID {inject_id}")
        inject = next((inject for inject in injects if inject['id'] == inject_id), None)

        if inject is None:
            print(f"[*] No inject found with ID {inject_id}")
            continue

        title = inject.get('title', 'No title')
        print(f"[PE.05] Executing inject {inject_id}: {title}")
        socketio.emit('message', {'data': f'Inject {inject_id} wird ausgeführt: {title}'})

        print("[PE.06] Waiting for 10 seconds")
        time.sleep(10)

    print("[*] Finished executing injects")
    return True



@app.route('/execute_exercise/<int:exercise_id>', methods=['POST'])
def execute_exercise(exercise_id):
    print(f"[*] execute_exercise called with exercise_id: {exercise_id}")

    print("[*] Loading exercise")
    exercise = load_exercise(exercise_id)

    # Check if the exercise exists
    if exercise is None:
        print("[*] Error: Exercise not found")
        return render_template('error.html', message="Exercise not found"), 404

    print("[*] Starting a new thread to perform the exercise")
    # Perform the exercise in a separate thread
    thread = Thread(target=perform_exercise, args=(exercise,))
    thread.start()

    print("[*] Rendering the executed_exercise.html page")
    # Render the executed_exercise.html page immediately
    return render_template('executed_exercise.html', exercise=exercise, status="Exercise is being executed")



@app.route('/update_comment', methods=['POST'])
def update_comment():
    logging.info('[UC.1] update_comment function called')

    try:
        data = request.get_json()
        logging.info(f'[UC.2] Received data: {data}')

        if 'id' in data and 'index' in data and 'comment' in data:
            try:
                exercise_id = int(data['id'])
                inject_index = int(data['index'])
                logging.info(f'[UC.3] Converting id and index to integer, exercise_id: {exercise_id}, inject_index: {inject_index}')
            except ValueError:
                logging.error('[*] Error: Invalid type for id or index')
                return jsonify({'status': 'error', 'message': 'Invalid type for id or index'})

            comment = data['comment']
            logging.info(f'[UC.4] Exercise ID: {exercise_id}, Inject Index: {inject_index}, Comment: {comment}')

            try:
                exercises = load_json('exercises.json')
                logging.info(f'[UC.5] Loaded exercises: {exercises}')
            except FileNotFoundError:
                logging.error('[*] Error: exercises.json file not found')
                return jsonify({'status': 'error', 'message': 'File not found'})
            except json.JSONDecodeError:
                logging.error('[*] Error: JSON decode error')
                return jsonify({'status': 'error', 'message': 'Error reading JSON file'})

            # Suche nach der Übung mit der entsprechenden ID
            exercise = None
            for ex in exercises:
                if ex['id'] == exercise_id:
                    exercise = ex
                    break

            if exercise:
                if 'inject_comment' not in exercise or not isinstance(exercise['inject_comment'], dict):
                    exercise['inject_comment'] = {}
                elif isinstance(exercise['inject_comment'], list):
                    # Konvertiere die Liste zu einem Wörterbuch
                    inject_comment_dict = {}
                    for i, val in enumerate(exercise['inject_comment']):
                        inject_comment_dict[str(i)] = val
                    exercise['inject_comment'] = inject_comment_dict
                
                exercise['inject_comment'][str(inject_index)] = comment
                logging.info(f'[UC.6] Updated inject_comment: {exercise["inject_comment"]}')
                logging.info(f'[UC.7] Updated exercise object: {exercise}')

                # Speichern der gesamten Liste zurück in die JSON-Datei
                try:
                    save_json('exercises.json', exercises)
                except IOError:
                    logging.error('[*] Error: Unable to write to exercises.json file')
                    return jsonify({'status': 'error', 'message': 'Unable to write to file'})

                logging.info('[UC.8] Saved exercises back to JSON file')

                return jsonify({'status': 'success'})
            else:
                logging.error(f'[*] Error: Exercise not found. Received id: {exercise_id}')
                return jsonify({'status': 'error', 'message': 'Exercise not found'})
        else:
            logging.error(f'[*] Error: Missing key in data. Received data: {data}')
            return jsonify({'status': 'error', 'message': 'Missing key in data'})

    except Exception as e:
        logging.error(f'[*] Error: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Internal server error'})






#### I N J E C T S ####

@app.route('/edit_inject_form/<int:inject_id>')
def edit_inject_form(inject_id):
    inject = get_inject_by_id(inject_id)
    if inject is None:
        return "Inject not found", 404
    scenarios = load_json('scenarios.json')
    return render_template('edit_inject.html', inject=inject, scenarios=scenarios)

@app.route('/execute_inject_form')
def execute_inject_form():
    return render_template('execute_exercise.html')





@app.route('/schedule_exercise', methods=['POST'])
def schedule_exercise():
    data = request.json
    exercises = load_json('exercises.json')
    exercises.append(data)
    save_json('exercises.json', exercises)
    if data['type'] == 'timed':
        schedule_timed_exercise(data)
    return jsonify({"status": "scheduled"}), 200

def schedule_timed_exercise(exercise):
    injects = load_json('injects.json')
    for idx, inject_idx in enumerate(exercise['inject_order']):
        inject = injects[inject_idx]
        delay = idx * exercise['interval'] * 60  # convert minutes to seconds
        Timer(delay, execute_inject, [inject]).start()

@app.route('/execute_inject/<exercise_name>/<inject_idx>')
def execute_inject_route(exercise_name, inject_idx):
    exercises = load_json('exercises.json')
    injects = load_json('injects.json')
    exercise = next((ex for ex in exercises if ex['name'] == exercise_name), None)
    if exercise:
        inject = injects[int(inject_idx)]
        execute_inject(inject)
    return jsonify({"status": "executed"}), 200

def execute_inject(inject):
    # Simulate sending inject via the specified communication type
    print(f"Executing inject: {inject['title']} via {inject['communication_type']}")
    # In real implementation, send email, text, call, or personal notification here


@app.route('/edit_inject/<int:inject_id>', methods=['GET', 'POST'])
def edit_inject(inject_id):
    # Hier holen Sie das Inject aus Ihrer Datenbank
    inject = get_inject_by_id(inject_id)

    scenarios = load_json('scenarios.json')  # Laden Sie die Szenarien aus der JSON-Datei
    # Die ganze json wird geladen
    injects = load_json('injects.json')

    # Überprüfen Sie, ob das Inject existiert
    if inject is None:
        return "Inject not found", 404

    if request.method == 'POST':

        # Das was aus dem Webformular kommt, wird in data gespeichert
        data = request.get_json()
                
        # Debugging-Ausgabe
        print("Received data:", data)
        
        # Aktualisieren Sie das Inject mit den neuen Daten aus dem Webformular
        updated_inject = {
            'id': inject_id,
            'title': data.get('title', inject['title']),
            'description': data.get('description', inject['description']),
            'exercise_benefit': data.get('exercise_benefit', inject['exercise_benefit']),
            'expected_response': data.get('expected_response', inject['expected_response']),
            'communication_type': data.get('communication_type', inject['communication_type']),
            'assigned_scenarios': data.get('assigned_scenarios', inject['assigned_scenarios'])
        }
        
        # Suchen Sie das Inject mit der entsprechenden ID und aktualisieren Sie es
        inject_index = next((index for (index, d) in enumerate(injects) if d['id'] == inject_id), None)
        
        if inject_index is not None:
            injects[inject_index] = updated_inject
        else:
            return "Inject not found in database", 404

        # Speichern Sie die Daten, nachdem alle Änderungen vorgenommen wurden
        save_json('injects.json', injects)
        
        # Debugging-Ausgabe
        print("[*] Updated inject:", updated_inject)

    # Rendern Sie die Bearbeitungsseite mit dem Inject als Kontext
    #return render_template('edit_inject.html', inject=inject)
    return render_template('edit_inject.html', inject=inject, scenarios=scenarios)
    

@app.route('/edit_injectBAK/<int:inject_id>', methods=['GET', 'POST'])
def edit_injectBAK(inject_id):
    # Hier holen Sie das Inject aus Ihrer Datenbank
    inject = get_inject_by_id(inject_id)

    # Überprüfen Sie, ob das Inject existiert
    if inject is None:
        return "Inject not found", 404

    if request.method == 'POST':
        # Die ganze json wird geladen
        injects = load_json('injects.json')

        # Das was aus dem Webformular kommt, wird in data gespeichert
        data = request.get_json()
    
        # Konvertieren Sie die inject_id in eine Zahl
        inject_id = int(data.get('id', inject['id']))
        
        # Debugging-Ausgabe
        # Zeigt die Webform Daten an
        print("Received data:", data)
    
        # Aktualisieren Sie das Inject mit den neuen Daten aus dem Webformular
        inject['id'] = int(data.get('id', inject['id']))
        inject['title'] = data.get('title', inject['title'])
        inject['description'] = data.get('description', inject['description'])
        print("[*] DESCRIPTION:", data.get('description', inject['description']))
        inject['exercise_benefit'] = data.get('exercise_benefit', inject['exercise_benefit'])
        inject['expected_response'] = data.get('expected_response', inject['expected_response'])
        inject['communication_type'] = data.get('communication_type', inject['communication_type'])
        inject['assigned_scenarios'] = data.get('assigned_scenarios', inject['assigned_scenarios'])
        
        # Speichern Sie das aktualisierte Inject in der Datenbank "injects.json"
        injects[inject_id] = inject
        print("[*] INJECTS:", injects[inject_id])

    
        # Speichern Sie die Daten, nachdem alle Änderungen vorgenommen wurden
        save_json('injects.json', injects)
    
        # Debugging-Ausgabe
        print("[*] Updated inject:", inject)
        
        injects = None
        injects = load_json('injects.json')
        print("[*] RELOEDED INJECT:", injects[inject_id])

    
    # Rendern Sie die Bearbeitungsseite mit dem Inject als Kontext
    return render_template('edit_inject.html', inject=inject)



@app.route('/save_exercise_order', methods=['POST'])
def save_exercise_order():
    data = request.json
    exercises = load_json('exercises.json')
    exercise = next((ex for ex in exercises if ex['name'] == data['exercise_name']), None)
    if exercise:
        exercise['inject_order'] = data['order']
        save_json('exercises.json', exercises)
    return jsonify({"status": "success"}), 200

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
    if request.method == 'GET':
        return jsonify(load_json('scenarios.json'))
    elif request.method == 'POST':
        data = request.json
        save_json('scenarios.json', data)
        return jsonify({"status": "success"}), 200

@app.route('/api/reports', methods=['GET', 'POST'])
def api_reports():
    if request.method == 'GET':
        return jsonify(load_json('reports.json'))
    elif request.method == 'POST':
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
    #app.run(debug=True, port=5010)
    socketio.run(app, debug=True, host="0.0.0.0", port=5010)


