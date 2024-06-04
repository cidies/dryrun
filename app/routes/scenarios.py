from flask import Blueprint, render_template
from app.utils.json_utils import load_json

scenarios_bp = Blueprint('scenarios', __name__)

@scenarios_bp.route('/scenarios')
def scenarios():
    scenarios = load_json('scenarios.json')
    return render_template('scenarios.html', scenarios=scenarios)

@scenarios_bp.route('/edit_scenario/<id>')
def edit_scenario(id):
    scenario = load_scenario(id)
    if scenario is not None:
        return render_template('edit_scenario.html', scenario=scenario)
    else:
        return "Scenario not found", 404

def load_scenario(id):
    scenarios = load_json('scenarios.json')
    for scenario in scenarios:
        if scenario['id'] == int(id):
            return scenario
    return None
