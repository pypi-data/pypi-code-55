from flask import Flask, request
from flask_cors import CORS #, cross_origin
import json
from .ledger_exec import LedgerExecutor

app = Flask(__name__)
CORS(app)
#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/accounts")
def accounts():
    params = "accounts"
    ledger = LedgerExecutor(app.logger)
    result = ledger.run(params)
    
    return f'accounts: {result}'

@app.route("/balance")
def balance():
    params = "b --flat --no-total"
    ledger = LedgerExecutor(app.logger)
    result = ledger.run(params)
    
    return result

@app.route("/currentValues")
def currentValues():
    root = request.args.get('root')
    currency = request.args.get('currency')
    params = f"b ^{root} -X {currency} --flat --no-total"

    ledger = LedgerExecutor(app.logger)
    result = ledger.run(params)
    
    #return f"current values for {root} in {currency}: {result}"
    return result

@app.route("/lots")
def lots():
    from .lots_parser import LotParser

    symbol = request.args.get('symbol')

    parser = LotParser(app.logger)
    result = parser.get_lots(symbol)

    return json.dumps(result)

@app.route('/securitydetails')
def security_details():
    ''' Displays the security details (analysis) '''
    from .sec_details import SecurityDetails

    symbol = request.args.get('symbol')
    currency = request.args.get('currency')

    x = SecurityDetails(app.logger, symbol, currency)
    result = x.calculate()

    return json.dumps(result)

@app.route('/about')
def about():
    ''' display some diagnostics '''
    import os
    cwd = os.getcwd()
    return f"cwd: {cwd}"

###################################

def run_server():
    """ Available to be called from outside """
    # use_reloader=False port=23948
    app.run(host='0.0.0.0', threaded=True, use_reloader=False, debug=True)
    # host='127.0.0.1' host='0.0.0.0'
    # , debug=True
    # Prod setup: 
    # debug=False


##################################################################################
if __name__ == '__main__':
    # Use debug=True to enable template reloading while the app is running.
    # debug=True <= this is now controlled in config.py.
    run_server()