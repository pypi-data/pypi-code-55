# -*- coding: utf-8 -*-
"""
EmberFactory / site navigation: manages the pages that are not directly related to ember production

Written as a flask Blueprint; if revising the app structure is desired, consider reading
https://stackoverflow.com/questions/24420857/what-are-flask-blueprints-exactly

Copyright (C) 2020  philippe.marbaix@uclouvain.be
"""

from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import current_app
from flask import send_from_directory
import os
from embermaker import makember as mke
from emberweb.__init__ import __version__
from markdown import markdown

bp = Blueprint("sitenav", __name__)

@bp.route("/")
def index():
    return render_template("emberweb/start.html", version = __version__, mkeversion = mke.__version__)

#Enable downloading examples:
@bp.route('/examples/<path:filename>', methods=['GET', 'POST'])
def examples_fil(filename):
    examples_dir = os.path.join(current_app.root_path, "examples/")
    return send_from_directory(directory=examples_dir, filename=filename)

#Load the example page
#The description of examples is in a file formatted in markdown and included in the examples/ folder.
@bp.route('/examples', methods=['GET', 'POST'])
def examples():
    examples_page = os.path.join(current_app.root_path, 'examples/examples.md')
    with open(examples_page, "r", encoding="utf-8") as input_file:
        content = markdown(input_file.read())
    # Add code to transform links to buttons when at the beginning of a paragraph
    txbutton = 'class="btn" style="float: right;">\
        <svg class="icon" aria-hidden="true" style="padding-right: 0.5em;">\
        <use xlink:href="/static/icons.svg#download"></use></svg>'
    txmarker = '<p><a href'
    thesplit = content.split(txmarker)
    content = thesplit[0]
    for txfrag in thesplit[1:]:
        content += txmarker + txfrag.replace('>', txbutton, 1)
    # Introduce the optional application root path
    # (there might be something more elegant but I could not find it !
    # I tried a 'one-pass' nice-looking solution with regex found on the web, it was way slower)
    content = content.replace('/static/', url_for('static', filename=''))\
                     .replace('/examples', url_for('sitenav.examples'))\
                     .replace('/more', url_for('sitenav.more'))
    return render_template("emberweb/examples.html", content=content)

#Load the 'More information' page
@bp.route('/more')
def more():
    return render_template("emberweb/more.html")

#Browsers such as Safari still appear to ask for /favicon.ico in spite of receiving the link to the favicon.
#Even worse, Safari is asking for /favicon.ico at the root of the website,
#regardless of the application root (e.g. /favicon.ico instead of /emberfactory/favicon.ico) !
#Therefore, the following rarely helps.
#This happens when files are downloaded.
@bp.route('/favicon.ico')
def favicon():
    static_dir = os.path.join(current_app.root_path, "static/")
    return send_from_directory(directory=static_dir, filename='favicon.ico')