from flask import Blueprint, render_template, request, redirect, url_for
import json

config_bp = Blueprint('config', __name__)
config_path = 'c:\\temp\\config.json'

@config_bp.route('/edit_config', methods=['GET', 'POST'])
def edit_config():
    if request.method == 'POST':
        with open(config_path, 'r') as f:
            config = json.load(f)
        form_data = request.form.to_dict()
        config.update(form_data)
        with open(config_path, 'w') as f:
            json.dump(config, f)
        return redirect(url_for('config.edit_config'))
    else:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return render_template('config_form.html', config=config)
