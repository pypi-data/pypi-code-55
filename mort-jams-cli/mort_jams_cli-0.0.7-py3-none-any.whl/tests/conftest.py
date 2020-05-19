import pytest
import requests_mock
from mock import patch
from prodigyteams.utils import CLIConfig

broker_address = "http://localhost:8080"

identity_response = {
    "ok": True,
    "user": {
        "id": 17,
        "created": "2019-08-02T20:47:07",
        "updated": "2019-12-19T19:59:10",
        "group": 15,
        "unixperms": 480,
        "owner": 17,
        "name": "Sebastián Ramírez",
        "source": "google-oauth2|117823206414188386149",
        "org": 11,
        "email": "sebastian@explosion.ai",
        "picture": "https://lh6.googleusercontent.com/-m9dfMr3IXW4/AAAAAAAAAAI/AAAAAAAAAAc/i0elegLEg6M/photo.jpg",
        "verified": True,
        "preferences": {
            "themeColor": "#696cd4",
            "prodigyTheme": {
                "bgCard": "#ffffff",
                "colorText": "#222222",
                "bgCardTitle": "#583fcf",
                "colorCardTitle": "#ffffff",
                "bgHighlight": "#ffe184",
                "colorHighlightLabel": "#583fcf",
                "bgMeta": "#f6f6f6",
                "colorMeta": "#6e6e6e",
            },
            "showAnnotationTour": False,
        },
        "membership": 1,
    },
    "orgs": [
        {
            "id": 11,
            "created": "2019-07-31T18:04:01",
            "updated": "2019-08-26T16:55:09",
            "owner": 11,
            "name": "Explosion AI (staging)",
            "group": 3,
            "unixperms": 500,
        },
        {
            "id": 7,
            "created": "2019-01-25T20:45:33",
            "updated": "2019-08-26T16:55:09",
            "owner": 7,
            "name": "_s_ca_le_test_0rg",
            "group": 3,
            "unixperms": 500,
        },
    ],
    "users": [
        {
            "id": 16,
            "created": "2019-07-31T18:04:01",
            "updated": "2019-09-09T21:49:02",
            "group": 15,
            "unixperms": 480,
            "owner": 16,
            "name": "Justin DuJardin",
            "source": "google-oauth2|114536595476223282880",
            "org": 11,
            "email": "justin@explosion.ai",
            "picture": "https://lh3.googleusercontent.com/-uer8OSrlGEs/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rcvaVZGmM8AyR_de2F2d2YdxX2-CQ/photo.jpg",
            "verified": True,
            "preferences": {
                "themeColor": "#696cd4",
                "prodigyTheme": {
                    "bgCard": "#ffffff",
                    "colorText": "#222222",
                    "bgCardTitle": "#583fcf",
                    "colorCardTitle": "#ffffff",
                    "bgHighlight": "#ffe184",
                    "colorHighlightLabel": "#583fcf",
                    "bgMeta": "#f6f6f6",
                    "colorMeta": "#6e6e6e",
                },
                "showAnnotationTour": False,
            },
            "membership": 8,
        },
        {
            "id": 2,
            "created": "2018-12-21T21:17:01",
            "updated": "2020-02-25T19:40:41",
            "group": 15,
            "unixperms": 480,
            "owner": 2,
            "name": "Justin DuJardin",
            "source": "google-oauth2|106752321136837834232",
            "org": 11,
            "email": "justin@dujardinconsulting.com",
            "picture": "https://lh4.googleusercontent.com/-DG_VX88x21g/AAAAAAAAAAI/AAAAAAAAAAA/AKxrwcbhKWwh8Imuo1INh8IHA9WPxzhgdg/mo/photo.jpg",
            "verified": True,
            "preferences": {
                "themeColor": "#da294f",
                "prodigyTheme": {
                    "bgCard": "#ffffff",
                    "colorText": "#222222",
                    "bgCardTitle": "#583fcf",
                    "colorCardTitle": "#ffffff",
                    "bgHighlight": "#ffe184",
                    "colorHighlightLabel": "#583fcf",
                    "bgMeta": "#f6f6f6",
                    "colorMeta": "#6e6e6e",
                },
                "showAnnotationTour": False,
            },
            "membership": 1,
        },
        {
            "id": 17,
            "created": "2019-08-02T20:47:07",
            "updated": "2019-12-19T19:59:10",
            "group": 15,
            "unixperms": 480,
            "owner": 17,
            "name": "Sebastián Ramírez",
            "source": "google-oauth2|117823206414188386149",
            "org": 11,
            "email": "sebastian@explosion.ai",
            "picture": "https://lh6.googleusercontent.com/-m9dfMr3IXW4/AAAAAAAAAAI/AAAAAAAAAAc/i0elegLEg6M/photo.jpg",
            "verified": True,
            "preferences": {
                "themeColor": "#696cd4",
                "prodigyTheme": {
                    "bgCard": "#ffffff",
                    "colorText": "#222222",
                    "bgCardTitle": "#583fcf",
                    "colorCardTitle": "#ffffff",
                    "bgHighlight": "#ffe184",
                    "colorHighlightLabel": "#583fcf",
                    "bgMeta": "#f6f6f6",
                    "colorMeta": "#6e6e6e",
                },
                "showAnnotationTour": False,
            },
            "membership": 1,
        },
        {
            "id": 17,
            "created": "2019-08-02T20:47:07",
            "updated": "2019-12-19T19:59:10",
            "group": 15,
            "unixperms": 480,
            "owner": 17,
            "name": "Sebastián Ramírez",
            "source": "google-oauth2|117823206414188386149",
            "org": 11,
            "email": "sebastian@explosion.ai",
            "picture": "https://lh6.googleusercontent.com/-m9dfMr3IXW4/AAAAAAAAAAI/AAAAAAAAAAc/i0elegLEg6M/photo.jpg",
            "verified": True,
            "preferences": {
                "themeColor": "#696cd4",
                "prodigyTheme": {
                    "bgCard": "#ffffff",
                    "colorText": "#222222",
                    "bgCardTitle": "#583fcf",
                    "colorCardTitle": "#ffffff",
                    "bgHighlight": "#ffe184",
                    "colorHighlightLabel": "#583fcf",
                    "bgMeta": "#f6f6f6",
                    "colorMeta": "#6e6e6e",
                },
                "showAnnotationTour": False,
            },
            "membership": 1,
        },
    ],
    "projects": [
        {
            "id": 1681,
            "created": "2019-09-04T19:37:39",
            "updated": "2019-09-04T19:37:39",
            "owner": 11,
            "name": "Test Project",
            "description": "",
            "group": 7,
            "unixperms": 504,
        },
        {
            "id": 1712,
            "created": "2019-09-27T19:14:58",
            "updated": "2019-09-27T19:14:58",
            "owner": 11,
            "name": "Toxic Textcat",
            "description": "",
            "group": 7,
            "unixperms": 504,
        },
    ],
    "org_users": [
        {
            "id": 24,
            "created": "2019-07-31T18:04:01",
            "updated": "2019-07-31T18:04:01",
            "owner": 11,
            "user": 16,
            "membership": 15,
            "unixperms": 504,
            "group": 7,
        },
        {
            "id": 26,
            "created": "2019-07-31T18:07:44",
            "updated": "2019-07-31T18:07:44",
            "owner": 11,
            "user": 2,
            "membership": 14,
            "unixperms": 504,
            "group": 7,
        },
        {
            "id": 31,
            "created": "2019-09-05T00:51:08",
            "updated": "2019-09-05T00:51:08",
            "owner": 11,
            "user": 17,
            "membership": 14,
            "unixperms": 504,
            "group": 7,
        },
        {
            "id": 32,
            "created": "2019-09-24T15:53:38",
            "updated": "2019-09-24T15:53:38",
            "owner": 7,
            "user": 17,
            "membership": 14,
            "unixperms": 504,
            "group": 7,
        },
    ],
    "tasks": [
        {
            "id": "521b4ca6a6694217baeeab3c3df5d0da",
            "created": "2019-09-30T21:54:03",
            "updated": "2019-10-02T20:14:35",
            "owner": 11,
            "unixperms": 504,
            "group": 15,
            "project": 1681,
            "name": "Task",
            "recipe": {
                "type": "textcat",
                "strategy": "binary",
                "label": ["TEST"],
                "input": "Reddit Insults",
                "active_learning": False,
                "include_patterns": False,
                "include_model": False,
                "model": "english_small",
                "segment": True,
                "view_id": "text",
                "config_json": "{}",
                "goal": "nooverlap",
            },
            "state": "stopped",
        },
        {
            "id": "853a8ed36b13443281269aa6836788ac",
            "created": "2019-09-27T15:36:34",
            "updated": "2019-10-02T22:06:41",
            "owner": 11,
            "unixperms": 504,
            "group": 15,
            "project": 1681,
            "name": "Is Docs NER",
            "recipe": {
                "type": "ner",
                "strategy": "binary",
                "label": ["ORG"],
                "input": "Github Issues",
                "active_learning": True,
                "include_patterns": False,
                "include_model": True,
                "model": "english_small",
                "segment": True,
                "view_id": "text",
                "config_json": "{}",
                "goal": "nooverlap",
            },
            "state": "stopped",
        },
        {
            "id": "ad4387f94af9460994211daba2352ef7",
            "created": "2019-09-04T19:38:03",
            "updated": "2019-10-16T16:41:18",
            "owner": 11,
            "unixperms": 504,
            "group": 15,
            "project": 1681,
            "name": "Is Docs?",
            "recipe": {
                "type": "textcat",
                "strategy": "binary",
                "label": ["DOCS"],
                "input": "Github Issues",
                "active_learning": True,
                "include_patterns": False,
                "include_model": False,
                "model": "english_large",
                "segment": True,
                "view_id": "text",
                "config_json": "{}",
                "goal": "nooverlap",
            },
            "state": "stopped",
        },
        {
            "id": "c2d1b3d42b594dabac372f30e0ed93fa",
            "created": "2019-09-27T19:19:16",
            "updated": "2019-10-04T00:43:01",
            "owner": 11,
            "unixperms": 504,
            "group": 15,
            "project": 1712,
            "name": "Toxic Eval",
            "recipe": {
                "type": "textcat",
                "strategy": "binary",
                "label": ["TOXIC"],
                "input": "Reddit Insults",
                "active_learning": True,
                "include_patterns": False,
                "include_model": True,
                "model": "english_small",
                "segment": True,
                "view_id": "text",
                "config_json": "{}",
                "goal": "nooverlap",
            },
            "state": "stopped",
        },
        {
            "id": "c3c2c553902648e7a116e6daf8f6a5c7",
            "created": "2019-09-27T19:15:21",
            "updated": "2019-10-04T00:43:04",
            "owner": 11,
            "unixperms": 504,
            "group": 15,
            "project": 1712,
            "name": "Toxic",
            "recipe": {
                "type": "textcat",
                "strategy": "binary",
                "label": ["TOXIC"],
                "input": "Reddit Insults",
                "active_learning": True,
                "include_patterns": False,
                "include_model": True,
                "model": "english_small",
                "segment": True,
                "view_id": "text",
                "config_json": "{}",
                "goal": "nooverlap",
            },
            "state": "stopped",
        },
    ],
    "task_users": [],
    "brokers": [
        {
            "id": "4beb2321873f461cbea8f6082ac8a6b5",
            "created": "2020-02-26T12:57:14",
            "updated": "2020-02-26T13:17:45",
            "group": 15,
            "unixperms": 480,
            "owner": 11,
            "address": broker_address,
            "region": "us-west1",
            "zone": "us-west1-a",
            "state": "created",
            "cloud_id": "pam-broker-dev",
            "nova_id": 30283,
            "token": "testpamtoken",
        }
    ],
    "counts": {
        "projects": [
            {"id": "project=1681", "source": 1681, "type": "project", "count": 573},
            {"id": "project=1712", "source": 1712, "type": "project", "count": 13},
        ],
        "tasks": [
            {
                "id": "task=ad4387f94af9460994211daba2352ef7",
                "source": "ad4387f94af9460994211daba2352ef7",
                "type": "task",
                "count": 518,
            },
            {
                "id": "task=853a8ed36b13443281269aa6836788ac",
                "source": "853a8ed36b13443281269aa6836788ac",
                "type": "task",
                "count": 52,
            },
            {
                "id": "task=c3c2c553902648e7a116e6daf8f6a5c7",
                "source": "c3c2c553902648e7a116e6daf8f6a5c7",
                "type": "task",
                "count": 0,
            },
            {
                "id": "task=c2d1b3d42b594dabac372f30e0ed93fa",
                "source": "c2d1b3d42b594dabac372f30e0ed93fa",
                "type": "task",
                "count": 13,
            },
        ],
    },
}

broker_meta_response = {
    "install": "/var/cache/prodigy_broker_data",
    "sources": {
        "Reddit Insults": {
            "title": "Reddit Insults",
            "path": "sources/annotated_reddit-INSULT-textcat.jsonl",
            "loader": "",
            "options": {},
            "id": "Reddit Insults",
        },
        "Github Issues": {
            "title": "Github Issues",
            "path": "sources/annotated_github-issues-DOCUMENTATION-textcat.jsonl",
            "loader": "",
            "options": {},
            "id": "Github Issues",
        },
        "News Headlines": {
            "title": "News Headlines",
            "path": "sources/news_headlines.jsonl",
            "loader": "",
            "options": {},
            "id": "News Headlines",
        },
        "Inexistent Source": {
            "title": "Inexistent Source",
            "path": "sources/inexistent_source.jsonl",
            "loader": "",
            "options": {},
            "id": "Inexistent Source",
        },
    },
    "vectors": {
        "en_vectors_web_lg": {
            "name": "/usr/local/data/spacy-models/2.0.0/en_vectors_web_lg-2.0.0",
            "title": "English GloVe Vectors",
        }
    },
    "models": {
        "english_small": {
            "name": "/usr/local/data/spacy-models/2.2.5/en_core_web_sm",
            "title": "English (Small)",
        },
        "english_medium": {
            "name": "/usr/local/data/spacy-models/2.2.5/en_core_web_md",
            "title": "English (Medium)",
        },
        "english_large": {
            "name": "/usr/local/data/spacy-models/2.2.5/en_core_web_lg",
            "title": "English (Large)",
        },
        "is_docs_run": {
            "name": "models/is_docs_run",
            "title": "Is Docs run",
            "owner": 2,
        },
    },
    "patterns": [],
    "imports": [
        "imports/bully_ner.jsonl",
        "imports/toxic_textcat_eval.jsonl",
        "imports/toxic_textcat.jsonl",
    ],
    "problems": [
        {
            "name": "No Data error",
            "description": "An error with no extra data attached!",
        },
        {
            "name": "Source Not Found",
            "description": "The resource specified is not a file or directory",
            "data": {"type": "source", "path": "sources/inexistent_source.jsonl",},
        },
        {
            "name": "Cannot Load",
            "description": 'The resource "/usr/local/data/spacy-models/2.0.0/en_vectors_web_lg-2.0.0" does not appear to be loadable',
            "data": "en_vectors_web_lg",
        },
    ],
}


@pytest.fixture(autouse=True)
def req_mock_auth_broker():
    config = CLIConfig(
        api_host="http://localhost:8000",
        device_audience="https://api.ygiderp.biz",
        device_client_id="FpGUNrjsjz2MCaFNA9dK7SX8LiAMohmd",
        device_token_url="https://explosion.eu.auth0.com/oauth/token",
        device_code_url="https://explosion.eu.auth0.com/oauth/device/code",
    )
    patcher = patch("prodigyteams.utils.get_cli_config")
    mockfn = patcher.start()
    mockfn.return_value = config

    with requests_mock.Mocker() as m:
        m.post(f"{config.api_host}/v1/identity", json=identity_response)
        m.get(f"{broker_address}/api/v1/broker/meta", json=broker_meta_response)

        # Sources
        m.post(f"{broker_address}/api/v1/sources/upload", status_code=200)
        m.delete(f"{broker_address}/api/v1/sources/Reddit%20Insults", status_code=200)

        # Packages
        m.get(
            f"{broker_address}/api/v1/packages",
            json=[
                {"url": "prodigy/", "name": "prodigy", "uploaded": False},
                {"url": "prodigyteams/", "name": "prodigyteams", "uploaded": True},
            ],
        )
        m.post(f"{broker_address}/api/v1/models/upload")
        m.get(
            f"{broker_address}/api/v1/packages/prodigy/",
            json=[
                {
                    "name": "prodigy",
                    "url": "http://localhost:8080/api/pip/prodigy/download/prodigy-1.8.3-cp35.cp36.cp37-cp35m.cp36m.cp37m-macosx_10_13_x86_64.whl",
                    "filename": "prodigy-1.8.3-cp35.cp36.cp37-cp35m.cp36m.cp37m-macosx_10_13_x86_64.whl",
                },
                {
                    "name": "prodigy",
                    "url": "http://localhost:8080/api/pip/prodigy/download/prodigy-1.6.2.dev30-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                    "filename": "prodigy-1.6.2.dev30-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                },
                {
                    "name": "prodigy",
                    "url": "http://localhost:8080/api/pip/prodigy/download/prodigy-1.7.1-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                    "filename": "prodigy-1.7.1-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                },
                {
                    "name": "prodigy",
                    "url": "http://localhost:8080/api/pip/prodigy/download/prodigy-1.8.2-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                    "filename": "prodigy-1.8.2-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                },
                {
                    "name": "prodigy",
                    "url": "http://localhost:8080/api/pip/prodigy/download/prodigy-1.8.3-cp35.cp36.cp37-cp35m.cp36m.cp37m-win_amd64.whl",
                    "filename": "prodigy-1.8.3-cp35.cp36.cp37-cp35m.cp36m.cp37m-win_amd64.whl",
                },
                {
                    "name": "prodigy",
                    "url": "http://localhost:8080/api/pip/prodigy/download/prodigy-1.8.0.dev19-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                    "filename": "prodigy-1.8.0.dev19-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                },
                {
                    "name": "prodigy",
                    "url": "http://localhost:8080/api/pip/prodigy/download/prodigy-1.8.2.dev0-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                    "filename": "prodigy-1.8.2.dev0-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                },
                {
                    "name": "prodigy",
                    "url": "http://localhost:8080/api/pip/prodigy/download/prodigy-1.8.3-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                    "filename": "prodigy-1.8.3-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                },
                {
                    "name": "prodigy",
                    "url": "http://localhost:8080/api/pip/prodigy/download/prodigy-1.6.2.dev35-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                    "filename": "prodigy-1.6.2.dev35-cp35.cp36.cp37-cp35m.cp36m.cp37m-linux_x86_64.whl",
                },
            ],
        )
        m.get(
            f"{broker_address}/api/v1/packages/prodigy/download/prodigy-1.8.3-cp35.cp36.cp37-cp35m.cp36m.cp37m-macosx_10_13_x86_64.whl",
            text="filecontent",
        )
        m.delete(f"{broker_address}/api/v1/packages/dummy")

        # Login
        m.post(
            config.device_code_url,
            json={
                "device_code": "PGY-123",
                "user_code": "testusercode",
                "verification_uri": "http://example.com/verify",
                "interval": 5,
                "verification_uri_complete": "http://example.com/verify?code=PGY-123",
            },
        )
        m.post(config.device_token_url, json={"id_token": "testidtoken"})
        m.post(
            f"{config.api_host}/v1/api-token", json={"access_token": "pamaccesstoken"}
        )
        yield m
    mockfn.reset_mock()
