#! /usr/bin/env python3

import argparse
import configparser
import http.server
import os
import socketserver
import requests
from textwrap import dedent
from urllib.parse import urlencode, urlparse, parse_qs

class ScriptHandler(http.server.BaseHTTPRequestHandler):
    """ basic handler to obtain the code from the http request """

    def do_GET(self):

        code = parse_qs(urlparse(self.path).query).get('code')[0]
        message = dedent("""
            Hello, your code is {}.
            Press Ctrl-C in the terminal to abort the http server.
        """).format(code).strip()


        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(str.encode(message))
        return

def strava_config_seeder(configfile, section):
    """ script function to get the strava data we need and generate config """

    # init the empty config
    config = configparser.ConfigParser()

    # if the config file exists, read it
    if os.path.isfile(configfile):
        config.read(configfile)

    # create the section if it doesn't exist.
    if not config.has_section(section):
        config.add_section(section)

    # read the client_id and client_secret.  Prompt for them if missing.
    get_config_items = ['client_id', 'client_secret']
    for i in get_config_items:
        i_value = config.get(section, i, fallback=None)
        if not i_value:
            i_value = input("Please enter the api {}:".format(i))
            config.set(section, i, str(i_value).strip())

    # Get details for the http server.
    print("An http server will be started on this machine to catch the strava redirect.")
    http_hostname = input("Enter the hostname to be used in the redirect link [127.0.0.1]: ") or "127.0.0.1"
    http_port = int(input("Enter the listening port for the redirect link [7777]: ") or "7777")


    url = "https://www.strava.com/oauth/mobile/authorize?{}".format(urlencode({
        "client_id": config.get(section, "client_id"),
        "redirect_uri": "http://{host}:{port}".format(host=http_hostname, port=http_port),
        "response_type": "code",
        "approval_prompt": "auto",
        "scope": "activity:write,read",
    }))
    print()
    print("Please open up the following url in your browser: {}".format(url))
    print("Authrorize the app, which will redirect to the temporary http server.")
    print()

    with socketserver.TCPServer(("", http_port), ScriptHandler) as httpd:
        print("serving at port", http_port)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()

    print()
    strava_code = input("Please enter the code obtained from your browser:")

    r = requests.post("https://www.strava.com/api/v3/oauth/token", data={
        "client_id": config.get(section, "client_id"),
        "client_secret": config.get(section, "client_secret"),
        "code": strava_code,
        "grant_type": "authorization_code",
    })
    r.raise_for_status()

    rdata = r.json()
    config.set(section, "access_token", rdata.get("access_token"))
    config.set(section, "refresh_token", rdata.get("refresh_token"))
    config.set(section, "expires_at", str(rdata.get("expires_at")))

    with open(configfile, "w") as f:
        config.write(f)

    print("All done.  The config file has been written: {}".format(configfile))



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("configfile", type=str, help="Path to the config file you would like to use.")
    parser.add_argument("-s", "--section", type=str, default="strava", help="name of the section in the config file to use.")
    args = parser.parse_args()

    strava_config_seeder(args.configfile, args.section)
