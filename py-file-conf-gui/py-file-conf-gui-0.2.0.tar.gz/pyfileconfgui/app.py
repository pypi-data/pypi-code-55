import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def create_app() -> dash.Dash:
    app = dash.Dash('pyfileconf', external_stylesheets=external_stylesheets)
    app.config.suppress_callback_exceptions = True
    return app
