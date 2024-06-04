from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.json_utils import load_json, save_json
from app.utils.exercise_utils import load_exercise, perform_exercise
from flask_socketio import SocketIO

exercises_bp = Blueprint('exercises', __name__)
socketio = SocketIO()

@exercises_bp.route('/update_exercise/<id>', methods=['POST'])
def update_exercise(id):
    exercises = load_json('exercises.json')
    for exercise in exercises:
        if exercise['id'] == int(id):
            exercise['name'] = request.form['name']
            exercise['description'] = request.form['description']
            exercise['target_team'] = request.form['target_team']
            exercise['last_performed'] = request.form['last_performed']
            inject_order = request.form['inject_order'].split(',')
            exercise['inject_order'] = [int(i) for i in inject_order]
            save_json('exercises.json', exercises)
            flash('Exercise updated successfully')
            return redirect(url_for('exercises.exercises'))
    flash('Exercise not found')
    return redirect(url_for('exercises.exercises'))

@exercises_bp.route('/exercises')
def exercises():
    exercises = load_json('exercises.json')
    return render_template('exercises.html', exercises=exercises)

@exercises_bp.route('/execute_exercise/<int:exercise_id>', methods=['POST'])
def execute_exercise(exercise_id):
    exercise = load_exercise(exercise_id)
    if exercise is None:
        return render_template('error.html', message="Exercise not found"), 404
    thread = Thread(target=perform_exercise, args=(exercise,))
    thread.start()
    return render_template('executed_exercise.html', exercise=exercise, status="Exercise is being executed")
