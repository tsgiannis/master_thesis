# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import apps.config
from apps.home import blueprint
from flask import render_template, request,jsonify,session
from flask_login import login_required
from jinja2 import TemplateNotFound
import json

from . import blueprint
from ..main_code import *
from execute import execute
from ..utilities import *

#https://stackoverflow.com/questions/71285841/submit-flask-form-without-re-rendering-the-page#:~:text=If%20you%20want%20to%20submit,submitted%20in%20the%20same%20format.

@blueprint.route('/route',methods=['POST'])
def routename():
    #datasets, language_models, deep_learning = load_config()
    # Your JSON string
    #json_string = '[{"key1":"value1"},{"key2":"value2"},{"key3":"value3"}]'

    # Decode the JSON string to a Python data structure
    #decoded_data = json.loads(json_string)
    selected_options = json.loads(request.form.get('selections'))
    #print(selected_option          )
    #return jsonify({'status': 'success'})
    #return '', 204  # 204 status means 'No Content'
    df = execute(selected_options)
    table_html = df.to_html(classes='table table-bordered table-striped text-center', index=False).replace('<th>', '<th class="text-center" th style = "background-color: red">')

    # Render the template with the HTML content
    #return render_template('index.html', table_html=table_html)
    return render_template('home/predictions.html',  table_html=table_html)
    # Process the selected option as needed
    #return f'Selected option: {selected_option}'




@blueprint.route('/index')
@login_required
def index():

    #data = [{'name': 'red'}, {'name': 'green'}, {'name': 'blue'}]
    session['datasets'], session['language_models'], session['deep_learning'] = load_config()
    # contains_list_ = contains_list_recursive(datasets)
    # contains_list = contains_list_recursive(language_models)

    return render_template('home/index.html',selected_option = None, segment='index', **locals())


"""TODO https://jsfiddle.net/enzDx/5/"""


# https://stackoverflow.com/questions/63628163/trying-to-get-the-bootstrap-dropdown-button-text-to-change-to-the-item-selected


@blueprint.route('/<template>')
@login_required
def route_template(template):
    session['datasets'], session['language_models'], session['deep_learning'] = load_config()
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None



