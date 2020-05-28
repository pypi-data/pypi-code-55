#!python
import flask
import requests
from threading import Thread

import logging

log = logging.getLogger(__name__)
logging.getLogger("werkzeug").setLevel(logging.WARNING)

app = flask.Flask(__name__)
server = None


@app.route("/shutdown")
def shutdown():
    """ shutdown flask from inside a request """
    func = flask.request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()
    return "Server shutting down"


@app.route("/")
def status():
    """ render html page with tables showing queues, task summary, tasks """
    try:
        from .. import pipeline

        tables = []
        titles = []

        # tasks table
        df = pipeline.view()

        # task summary
        status = [
            "waiting",
            "ready",
            "workerq",
            "loading",
            "running",
            "saving",
            "completed",
            "failed",
            "failed_upstream",
            "total",
        ]
        if isinstance(df, str):
            titles.append("TaskDB")
            tables.append(df)
        else:
            # task summary
            summary = df.groupby("status")[["path"]].count().T
            summary.columns.name = None
            for col in set(status) - set(summary.columns):
                summary[col] = 0
            summary = summary.fillna(0)
            summary["total"] = summary.sum(axis=1)
            tables.append(summary[status].to_html(index=False, table_id="summary"))
            titles.append("Task count by status")
            tables.append(df.to_html(table_id="task"))
            titles.append("Task list")
    except Exception as e:
        log.exception("")
        return f"Error in server. {str(e)}"

    return flask.render_template("view.html", tables=tables, titles=titles)


# control tasks  #########################################################################


def start():
    """ start flask in thread """

    global server

    def target():
        """ start flask thread """
        try:
            # reduce verbosity
            import click

            def secho(*args, **kwargs):
                pass

            def echo(*args, **kwargs):
                pass

            click.echo = echo
            click.secho = secho

            app.run(debug=False)
        except:
            log.exception("error starting flask")

    if server:
        log.error("flask server already running")
        return
    log.info("starting web server")
    server = Thread(target=target, daemon=True, name=__name__)
    server.start()


def stop():
    """ close flask server """
    global server

    def target():
        """ close server via shutdown request """
        try:
            r = requests.get("http://localhost:5000/shutdown")
            r.raise_for_status()
        except:
            log.warning("web server not running")

    log.info("stopping web server")
    t = Thread(target=target, daemon=True, name=f"shutdown {__name__}")
    t.start()
    server = None


def restart():
    """ restart server """
    stop()
    start()


if __name__ == "__main__":
    """ for testing. normally run in background thread """
    app.run(debug=True)
