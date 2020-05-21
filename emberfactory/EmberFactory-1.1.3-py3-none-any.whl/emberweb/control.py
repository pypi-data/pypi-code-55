# -*- coding: utf-8 -*-
"""
                 EmberFactory / web application

This module manages the web application.
It is written as a flask Blueprint.
It works :-), but I not sure yet that this is a recommended use of a Blueprint.
It might be an acceptable structure as it avoids getting everything in __init__py, but
I do not see how it can be actually useful as a blueprint (= re-usable). See e.g.
# https://stackoverflow.com/questions/24420857/what-are-flask-blueprints-exactly

Copyright (C) 2020  philippe.marbaix@uclouvain.be
"""

from flask import Blueprint
from flask import render_template
from flask import request
from flask import current_app, session
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os, sys
import uuid
from embermaker import helpers as hlp
from embermaker import makember as mke
from emberweb.__init__ import __version__

bp = Blueprint("control", __name__)

@bp.route("/")
def index():
    return render_template("emberweb/start.html", version = __version__, mkeversion = mke.__version__)

@bp.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        return index()

    # Default message to be returned within the template
    message={"error":"", "log": [], "outfile": None, "runreport": ""}

    # File upload and embermaker run
    # ------------------------------
    global sesid
    hlp.startlog(web=True)
    try:
        # Store user choice about deleting files:
        session['delfile'] = request.form.get('delfile') != None
        # Get filename and check file
        fileitem = request.files['file']
        if not fileitem.filename:
            message["error"]="No file provided or bad file."
            return render_template("emberweb/error.html", message=message)
        fnamesplit = os.path.splitext(os.path.basename(fileitem.filename))
        # Reject file if the extension does not suggest an Excel file
        # (wile devils can masquerade as angels, this protects against potential evils who look like evils)
        if fnamesplit[1] not in ['.xls', '.xlsx']:
            message["error"] = "Unexpected file extension."
            return render_template("emberweb/error.html", message=message)

        #Generate a file path name containing a unique ID
        # (so files are always stored under different names + users cannot get somone else's file):
        sesid = str(uuid.uuid1())
        fnamesplit = os.path.splitext(os.path.basename(fileitem.filename))
        fname = secure_filename(fnamesplit[0] + "" + sesid + fnamesplit[1])
        infile = os.path.join(current_app.instance_path, 'in/', fname)
        # Upload file
        fileitem.save(infile)

        # Execution of makember (result = [fname, error-message-if-any])
        result = mke.makember(infile=infile, prefcsys=request.form['csys'])

        # Optionally delete file
        if session['delfile']:
            os.remove(infile)

        # An output file was generated (success!)
        if result[0] != None:
            # Provide a url for the download
            # Result[0] is the file's path on the server
            outfile = 'out/'+ os.path.basename(result[0])
            message["outfile"] = outfile # inserts url for download
            # Report logged messages
            message["log"] = hlp.getlog("full")
            runreport = ""
            warnings = hlp.getlog("warning")
            if len(warnings) > 0:
                runreport += "<h3>Warning message(s)</h3>" \
                   "Warning messages do not necessarily mean that there is an error, but  you should pay attention:"
                message["error"] = warnings
            critical = hlp.getlog("critical")
            if len(critical) > 0:
                runreport += "<h3>Critical issue message(s)</h3>" \
                   "This ember may contain errors and should not be published without investigating. "\
                   "The detected problem(s) are:"
                message["error"] = critical
            if len(runreport) == 0:
                runreport = "No warning messages, everything appears ok!"
            message["runreport"]= runreport

        # No file was generated: a fatal error occurred:
        else:
            message["error"] = "Execution generated the following message, then failed: " \
                + str(result[1])
            return render_template("emberweb/error.html", message=message)

    # An error occurred, and we did not handle it in any way:
    except Exception as exc:
        message["error"] = "An error for which there is no handling has occurred. " \
                           "We apologize. Any information would appear below:"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        hlp.addlogwarn(str(exc) + " Position: " + fname + ":" + str(exc_tb.tb_lineno), critical=True)
        message["log"] = hlp.getlog("full")
        return render_template("emberweb/error.html", message=message)

    return render_template("emberweb/result.html", message=message)

# Enable downloading results:
@bp.route('/out/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    dloads = os.path.join(current_app.instance_path, "out/")
    result = send_from_directory(directory=dloads, filename=filename)
    if session['delfile']:
        os.remove(os.path.join(dloads,filename))
    return result

# Enable downloading examples:
@bp.route('/examples/<path:filename>', methods=['GET', 'POST'])
def examples(filename):
    examples = os.path.join(current_app.root_path, "examples/")
    return send_from_directory(directory=examples, filename=filename)
