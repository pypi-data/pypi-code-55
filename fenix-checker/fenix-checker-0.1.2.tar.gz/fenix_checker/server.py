import json
from ipaddress import IPv4Address, IPv6Address
from sys import exit, stderr

import psycopg2
import yaml
from flask import Flask, Response, request

app = Flask(__name__)
application = app  # for uWSGI


def load_config(filename="config.yml"):
    try:
        conf_file = open(filename, "r")
    except FileNotFoundError:
        stderr.write(f"Config file ({filename}) not found.\n")
        exit(1)
    config = yaml.load(conf_file, Loader=yaml.SafeLoader)
    if "db" not in config:
        stderr.write("DB config not found in the configuration file.\n")
        exit(1)
    if set(["host", "port", "user", "password", "dbname"]) != set(config["db"]):
        stderr.write("Invalid DB config format.\n")
        exit(1)
    return config


def is_valid_ipv6_address(ip):
    try:
        addr = IPv6Address(ip)
    except ValueError:
        return False
    return addr.is_global


def is_valid_ipv4_address(ip):
    try:
        addr = IPv4Address(ip)
    except ValueError:
        return False
    return addr.is_global


def is_valid_ip_address(ip):
    return is_valid_ipv4_address(ip) or is_valid_ipv6_address(ip)


def json_response(content, status=200):
    return Response(json.dumps(content), status=status, headers={
        "Access-Control-Allow-Origin": "*",
        "Content-type": "application/json"
    })


@app.route("/", methods=["GET"])
def fenix():
    config = load_config()
    try:
        db_conn = psycopg2.connect(host=config["db"]["host"],
                                   port=config["db"]["port"],
                                   user=config["db"]["user"],
                                   password=config["db"]["password"],
                                   dbname=config["db"]["dbname"])

    except (psycopg2.OperationalError, psycopg2.DatabaseError):
        return json_response({"error": "Can't connect to DB"}, 400)

    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    if not is_valid_ip_address(ip):
        return json_response({"error": "Invalid IP"}, 400)
    db = db_conn.cursor()
    try:
        db.execute(f"SELECT 1 FROM networks WHERE inet '{ip}' << prefix")
    except (psycopg2.DataError, psycopg2.DatabaseError):
        return json_response({"error": "DB query error"}, 400)
    r = db.fetchall()
    db.close()
    if r == []:
        return json_response({"result": 0})
    elif int(r[0][0]) > 0:
        return json_response({"result": int(r[0][0])})
