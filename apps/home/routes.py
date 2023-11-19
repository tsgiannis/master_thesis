# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from ..main_code import *
from ..utilities import *


@blueprint.route('/index')
@login_required
def index():
    data = [{'name': 'red'}, {'name': 'green'}, {'name': 'blue'}]
    datasets, b, c = load_config()
    for dataset in datasets:
        for key in dataset:
            if 'link' in key:
                print('found')
            print(dataset[key])

    for key in datasets[0]:
        print(key)
        #print(d.name)
    return render_template('home/index.html', segment='index',**locals())


@blueprint.route('/<template>')
@login_required
def route_template(template):

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
