from flask import Blueprint, render_template

communication_bp = Blueprint('communication', __name__)

@communication_bp.route('/communication')
def communication():
    return render_template('communication.html')
