# pylint: disable=invalid-name

from flask import Flask, jsonify

from oautom.execution.bash_execution import BashExecution
from oautom import OAutom, Flow, OAutomMode

app = Flask(__name__)

oautom = OAutom(mode=OAutomMode.background)

flow1 = Flow('flow 1', app=oautom)
step1 = BashExecution('execution 1', flow=flow1, command='touch /tmp/file1')
step2 = BashExecution('sleep', flow=flow1, command='sleep 60')
step3 = BashExecution('execution 2', flow=flow1, command='touch /tmp/file2')
step2.depends(step1)
step3.depends(step2)
oautom.run()


@app.route("/flows")
def list_flow():
    return jsonify(oautom.flows())


@app.route("/logs")
def logs_flow():
    return jsonify(oautom.logs())


@app.route("/start/<flow>")
def start_flow(flow: str):
    result = ("OK", 200)
    if not oautom.start(flow):
        result = ("ALREADY RUNNING", 200)
    return result


@app.route("/status/<flow>")
def status_flow(flow: str):
    return jsonify(oautom.status(flow))


if __name__ == "__main__":
    app.run(debug=True)
