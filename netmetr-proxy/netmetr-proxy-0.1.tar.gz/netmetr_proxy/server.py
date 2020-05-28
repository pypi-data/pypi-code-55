# Copyright © CZ.NIC, z. s. p. o.
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, request, Response
from datetime import datetime
from sys import exit, stderr
import json
import calendar
import yaml
import re
import requests
from urllib.parse import quote

app = Flask(__name__)
application = app  # for uWSGI


def load_config(file="config.yml"):
    try:
        conf_file = open("config.yml", "r")
    except FileNotFoundError:
        stderr.write("Config file (config.yml) not found.\n")
        exit(1)
    config = yaml.load(conf_file, Loader=yaml.SafeLoader)
    try:
        backend = re.sub(r"([^/]$)", "\1/", config["backend_url"])  # adds a trailing slash if missing
        token = quote(config["token"])
    except KeyError:
        stderr.write("Missing config key. Both 'backend_url' and 'token' are required.\n")
        exit(1)
    return {
        "backend": backend,
        "token": token
    }


def parse_date(request):
    def get_int_param(request, name):
        return int(request.args.get(name))

    def valid_date(month, year):
        lastday = calendar.monthrange(year, month)[1]
        if datetime(year, month, lastday) > datetime.now():
            raise ValueError
        else:
            return {"month": month, "year": year}

    try:
        month = get_int_param(request, "month")
        year = get_int_param(request, "year")
        # check if date isn't current month (can't be approved/downloaded) or future:
        parsed = valid_date(month, year)
    except TypeError:
        return {"error": "Missing or invalid parameter (year, month)."}
    except ValueError:
        return {"error": "Invalid date (can't be a current of future month)."}
    else:
        return parsed


def err_response(message, status=400):
    return Response(json.dumps({"success": False, "error": message}),
                    status=status, mimetype="application/json")


def success_response(message):
    return Response(json.dumps({"success": True, "message": message}),
                    status=200, mimetype="application/json")


@app.route("/opendata", methods=["GET"])
def opendata():
    config = load_config()
    date = parse_date(request)
    if "error" in date:
        return err_response(date["error"])
    url = f"{config['backend']}RMBTStatisticServer/exportDirty/NetMetr-opendata-dirty-" \
          f"{date['year']}-{date['month']}.zip"
    r = requests.post(url, json={"key": config["token"]})
    if r.text.startswith("ERROR:"):
        return err_response(r.text.replace("ERROR: ", ""), 403)
    headers = {
        "Content-disposition": f"attachment; filename=NetMetr-opendata-dirty-{date['year']}-"
                               f"{str(date['month']).zfill(2)}.zip",
        "Content-type": "application/octet-stream",
        "Pragma": "no-cache",
        "Expires": 0,
    }
    return Response(r.content,
                    status=200,
                    mimetype="application/octet-stream",
                    headers=headers)


@app.route("/approve", methods=["GET"])
def approve():
    config = load_config()
    date = parse_date(request)
    if "error" in date:
        return err_response(date["error"])
    url = f"{config['backend']}RMBTStatisticServer/approve"
    r = requests.post(url,
                      json={
                          "key": config["token"],
                          "month": date["month"],
                          "year": date["year"]
                      }
                      )
    if r.text.startswith("ERROR:"):
        return err_response(r.text.replace("ERROR: ", ""), 403)
    if r.text.startswith("OK:"):
        try:
            num = int(r.text.replace("OK: ", ""))
        except ValueError:
            return err_response(f"Unable to parse the server response: '{r.text}'", 500)
        if num == 0:
            return success_response(f"Results for {date['year']}-{str(date['month']).zfill(2)} were"
                                    f" probably already approved before.")
        if num > 0:
            return success_response(f"Results for {date['year']}-{str(date['month']).zfill(2)} were"
                                    f" successfully approved.")
        if num < 0:
            return err_response("Server says it approved negative number of results o.O", 500)
