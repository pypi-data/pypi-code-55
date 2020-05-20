from zlibtui import app


def main():
    myApp = app.App()
    myApp.main()
    print(app.term.home + app.term.clear)
