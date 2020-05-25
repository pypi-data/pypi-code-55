import os
import json
import firebase_admin
from firebase_admin import auth, credentials
from meeshkan_hosted_secrets import access_secret_string


def verify_token(id_token):
    try:
        verify_token._firebase_initiated
    except AttributeError:
        if os.environ.get("GAE_ENV") == "standard":
            # App engine production
            firebase_credentials = access_secret_string("firebase-adminsdk-credentials")
            cred = credentials.Certificate(json.loads(firebase_credentials))
        else:
            from pathlib import Path
            cred = credentials.Certificate(
                str(Path.home())
                + os.sep
                + ".meeshkan"
                + os.sep
                + "firebase-adminsdk-credentials.json"
            )
        firebase_admin.initialize_app(cred)
        verify_token._firebase_initiated = True

    return auth.verify_id_token(id_token)
