# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask_sqlalchemy import SQLAlchemy

import apps.config
from apps.home import blueprint
from flask import render_template, request, jsonify, session
from flask_login import login_required
from jinja2 import TemplateNotFound
import json

from . import blueprint
from ..main_code import *
from execute import execute
from ..utilities import *
from ..text_analysis import *
from ..extensions import db


# https://stackoverflow.com/questions/53921939/bootstrap-4-2-1-failed-to-execute-queryselector-on-document-javascriptv

# app = Flask(__name__)
# db = SQLAlchemy(app)

class LoggingDetails(db.Model):
    __tablename__ = 'LoggingDetails'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    LoggingID = db.Column(db.Text, nullable=False)
    PatentCode = db.Column(db.Text, nullable=False)
    Relevance = db.Column(db.Integer)


@blueprint.route('/save_to_database', methods=['POST'])
def save_to_database():
    table_data = request.json
    for row in table_data:
        loggingID = row['LoggingID']
        patentCode = row['PatentCode']
        relevance = row['Relevance']
        new_loggingDetails = LoggingDetails(LoggingID=loggingID, PatentCode=patentCode, Relevance=relevance)
        db.session.add(new_loggingDetails)
    db.session.commit()
    return 'Data saved to database successfully'


@blueprint.route('/get_filtered_options', methods=['POST'])
def get_filtered_options():
    selected_value = request.json['selectedValue']
    return_values = get_value_for_key_in_list_of_dictionaries(session['datasets'], 'name', selected_value)
    return_list = [item.lower().replace(',', '') for item in return_values.split()]
    session['sections'] = return_list
    dropdown_options_html = ''
    for item in session['sections']:
        if item.lower() not in session['dynamic.sections']:
            dropdown_options_html += f'<a href="#"  class="disabled">' + item + '</a>'
        else:
            dropdown_options_html += f'<a href="#" data-value="' + item +'" onclick="selectedOption(this)">'+ item + '</a>'
    return dropdown_options_html
    # return jsonify({'success': True})


# https://stackoverflow.com/questions/71285841/submit-flask-form-without-re-rendering-the-page#:~:text=If%20you%20want%20to%20submit,submitted%20in%20the%20same%20format.

@blueprint.route('/route', methods=['POST'])
def routename():
    # datasets, language_models, deep_learning = load_config()
    # Your JSON string
    # json_string = '[{"key1":"value1"},{"key2":"value2"},{"key3":"value3"}]'

    # Decode the JSON string to a Python data structure
    # decoded_data = json.loads(json_string)
    selected_options = json.loads(request.form.get('selections'))
    # print(selected_option          )
    # return jsonify({'status': 'success'})
    # return '', 204  # 204 status means 'No Content'
    meaningful, meaningless = keywords_processing(get_value_out_of_list_of_dicts(selected_options, 'keywords'))
    selected_options = replace_dictionary_value(selected_options, 'keywords', ' '.join(meaningful))

    df = execute(selected_options)
    # Add new columns with checkboxes
    # df[
    #  'Success'] = '<input type="checkbox" class="custom-checkbox" onclick="toggleCheckmark(this)" data-result="success">'
    # df[
    # 'Failure'] = '<input type="checkbox" class="custom-checkbox" onclick="toggleCheckmark(this)" data-result="failure">'
    # df['RelIR'] = '< input type = "checkbox" class="flipswitch" >'
    # df['Success'] += '<span class="checkmark">✔️</span>'
    # df['Failure'] += '<span class="checkmark">❌</span>'

    table_html = df.to_html(classes='table table-bordered table-striped text-center', index=False,
                            escape=False).replace('<th>', '<th class="text-center" th style = "background-color: red">')

    # Render the template with the HTML content
    # return render_template('index.html', table_html=table_html)
    return render_template('home/predictions.html', dataframe=df)
    # Process the selected option as needed
    # return f'Selected option: {selected_option}'


@blueprint.route('/api/keyword_processing', methods=['POST'])
def functionality_check():
    keywords_dict = {}

    meaningful, meaningless = keywords_processing(request.get_json()['keywords'])
    keywords_dict['meaningful'] = meaningful
    keywords_dict['meaningless'] = meaningless
    return jsonify(keywords_dict)


@blueprint.route('/index')
@login_required
@read_directory(directory_name='resources')
def index():
    directory_contents = session.get('directories', [])
    # methods
    # languagemodels
    # datasets
    # ipclevels
    # patentsections
    # noofwords
    # singlemulti
    # structure
    # ensemble
    session['methods'], session['languagemodels'], session['datasets'], session['ipclevels'], \
    session['noofwords'], session['singlemulti'], session['structures'], session['ensemble'] = load_config()
    session['sections'] = 'Please Select Dataset'.split()
    # contains_list_ = contains_list_recursive(datasets)
    # contains_list = contains_list_recursive(language_models)

    return render_template('home/index.html', selected_option=None, segment='index', **locals())


"""TODO https://jsfiddle.net/enzDx/5/"""


# https://stackoverflow.com/questions/63628163/trying-to-get-the-bootstrap-dropdown-button-text-to-change-to-the-item-selected


@blueprint.route('/<template>')
@login_required
def route_template(template):
    session['datasets'], session['language_models'], session['methods'], session['ipcs'], session[
        'single_multi'] = load_config()
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
