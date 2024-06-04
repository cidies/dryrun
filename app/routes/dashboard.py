from flask import Blueprint, render_template
from app.utils.json_utils import load_json

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    notifications = load_json('notifications.json')
    exercises = load_json('exercises.json')
    return render_template('dashboard.html', notifications=notifications, exercises=exercises)
