from flask import Blueprint, render_template
from app.utils.json_utils import load_json

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
def reports():
    reports = load_json('reports.json')
    return render_template('reports.html', reports=reports)
