"""
Set of tools to handle the connection settings.
"""
import random
import os
from socket import gethostname
import argparse
import shutil
import json
import webbrowser
import logging
from OpenSSL import crypto
from flask import Flask, redirect, request
import requests

CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"
CONFIG_FILE = "config.json"
CONFIG_TEMPLATE = {
    "client_secret": "",
    "client_id": "",
    "domain": "mybraincube.com",
    "verify": True,
}
SCOPES = "BASE%20API"
PORT = 5000
LOCALHOST = "https://localhost:{}/".format(PORT)
SUCCESS_MESSAGE = "Braincube connector token was retrieved!"
CLOSING = """
<!doctype html>
<html lang="en">
<body>
  <center>
    <img src="https://www.braincube.com/wp-content/uploads/2015/12/Braincube-logo-carre.png">
    <p style="font-size:60px;color:green">✓</p>
    <div style="font-size:30px">{message}</div>
    <div style="font-size:30px">You can now close this page</div>
  </center>
</body>
</html>
""".format(
    message=SUCCESS_MESSAGE
)

LOGGER = logging.getLogger(__name__)


def yesno_question(question):
    """Query the user with a yes/no question. The default value is yes

    :param question: Text of the question
    :type question: str
    :returns: True for yes and False for no
    :rtype: bool

    """
    positive_answers = ["YES", "Y", ""]
    negative_answers = ["NO", "N"]
    answer = None
    while answer not in positive_answers + negative_answers:
        answer = input(" - {} [Y]es/no:".format(question)).upper()
    if answer in positive_answers:
        return True
    return False


def generate_ssl_certificate(config_dir):
    """Generate a certificate ssl and a key ssl file in the configuration directory

    :param config_dir: path of the configuration directory
    :type config_dir: str
    :returns: None

    """

    if not os.path.exists(os.path.join(config_dir, CERT_FILE)) or not os.path.exists(
        os.path.join(config_dir, KEY_FILE)
    ):
        # create a key pair
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)
        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "FR"  # country code
        cert.get_subject().L = "Issoire"  # locality
        cert.get_subject().OU = "Braincube"  # organisation
        cert.get_subject().CN = gethostname()
        cert.set_serial_number(random.getrandbits(128))
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)

        cert.sign(key, "sha256")
        open(os.path.join(config_dir, CERT_FILE), "wb").write(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
        )
        open(os.path.join(config_dir, KEY_FILE), "wb").write(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
        )


def fill_config_template(config_dir):
    """Fill in the CONFIG_TEMPLATE and write down the CONFIG_FILE file

    :param config_dir: path of the configuration directory
    :type config_dir: str
    :returns: Output whether the configuration directory was created as expected
    :rtype: bool

    """
    config = dict(CONFIG_TEMPLATE)
    config["client_id"] = input(" - Braincube application Client ID:")
    config["client_secret"] = input(" - Braincube application Client Secret:")
    with open(os.path.join(config_dir, CONFIG_FILE), "w") as config_file:
        json.dump(config, config_file)


def create_config_dir(config_dir):
    """Create a configuration directory

    :param config_dir: path of the configuration directory
    :type config_dir: str
    :returns: Output whether the configuration directory was created as expected
    :rtype: bool
    """
    if os.path.exists(config_dir):
        answer = yesno_question("Overwrite {}".format(config_dir))
        if not answer:
            return False
        shutil.rmtree(config_dir)
    os.mkdir(config_dir)
    generate_ssl_certificate(config_dir)
    fill_config_template(config_dir)
    return True


def read_config(config_dir):
    """Reads CONFIG_FILE and return the configuration

    :param config_dir: path of the configuration directory
    :type config_dir: str
    :returns: configuration dictionary
    :rtype: dictionary
    """
    with open(os.path.join(config_dir, CONFIG_FILE), "r") as config_file:
        config = json.load(config_file)
    return config


def build_connect_url(config):
    """Builds the url to connect via the braincube authorization

    :param config: configuration dictionary
    :type config: dictionary
    :returns: braincube authorization url
    :rtype: str
    """
    authorize_url = "https://{domain}/sso-server/vendors/braincube/authorize.jsp"
    authorize_url = authorize_url.format(domain=config.get("domain"))
    redirect_url = LOCALHOST + "token"
    arguments = (
        "?client_id={id}&response_type=code&scope={scope}&redirect_uri={redirect}"
    )
    arguments = arguments.format(
        **{"id": config.get("client_id"), "scope": SCOPES, "redirect": redirect_url}
    )
    url = authorize_url + arguments
    return url


def build_token_url(config):
    """Builds the url to connect via the braincube authorization

    :param config: configuration dictionary
    :type config: dictionary
    :returns: braincube authorization url
    :rtype: str
    """
    token_url = "https://{domain}/sso-server/ws/oauth2/token"
    token_url = token_url.format(domain=config.get("domain"))
    return token_url


def shutdown_server():
    """Shutdown the server after the job is done.
    """
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


def create_app(config):
    """Builds a flask app that redirect the user to the braincube login page

    :param config: configuration dictionary
    :type config: dictionary
    """
    app = Flask(__name__)
    setattr(app, "bc_config", config)

    @app.route("/")
    def launch_authentication():
        """ Opens braincube authenticfication page
        """
        request_url = build_connect_url(app.bc_config)
        return redirect(request_url)

    @app.route("/token")
    def get_token():
        """Use the the code provided with the redirect link to request the token."""
        config = app.bc_config
        code = request.url.split("code=")[1]
        content = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": LOCALHOST + "token",
            "client_id": config.get("client_id"),
            "client_secret": config.get("client_secret"),
        }
        token_url = build_token_url(config)
        token_data = requests.post(token_url, data=content, verify=config.get("verify"))
        if token_data.status_code != 200:
            error_log = "Requesting the token failed with error code {}"
            error_log = error_log.format(token_data.status_code)
            LOGGER.error(error_log)
        token_data = json.loads(token_data.text)
        token = token_data.get("access_token")
        config_dir = config.get("directory")
        with open(os.path.join(config_dir, CONFIG_FILE), "r") as config_file:
            config = json.load(config_file)
        config.update({"oauth2_token": token})
        with open(os.path.join(config_dir, CONFIG_FILE), "w") as config_file:
            json.dump(config, config_file)
        LOGGER.info(SUCCESS_MESSAGE)
        return redirect(LOCALHOST + "close")

    @app.route("/close")
    def render_close():
        """ Display the success message
        """
        shutdown_server()
        return CLOSING

    return app


def request_token(config):
    """Request a token from the braincube website
    :param config: configuration dictionary
    :type config: dictionary
    :returns: a token
    :rtype: str
    """
    app = create_app(config)
    webbrowser.open(LOCALHOST)
    config_dir = config.get("directory")
    app.run(
        port=PORT,
        debug=False,
        ssl_context=(config_dir + os.sep + "cert.pem", config_dir + os.sep + "key.pem"),
    )


def main():
    """Manages the process of creating a new configuration directory from checking if one already
    exists to creating the configuration files.

    :returns: Output whether the action was run succesfully.
    :rtype: bool

    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--create", action="store_true", help="Create a new configuration"
    )
    parser.add_argument("-t", "--token", action="store_true", help="Get the token")
    parser.add_argument(
        "-p", "--path", type=str, help="Path to the configuration directory"
    )
    args = parser.parse_args()

    ## Set the config path
    config_dir = args.path
    if config_dir is None:
        config_dir = os.path.join(os.path.expanduser("~"), ".braincube")

    ## Create a new configuration
    if args.create:
        success_config = create_config_dir(config_dir)
        if not success_config:
            return False

    ## Request a token
    if args.token:
        config = read_config(config_dir)
        config["directory"] = config_dir
        request_token(config)
    return True


if __name__ == "__main__":
    main()
