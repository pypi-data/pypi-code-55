import time
import suanpan
from suanpan.app import app

@app.trigger.interval(1)
def test2(context):
    value = int(time.time())
    gqwe = app.vars.Int("qwe")
    gqwe.set(value)
    qwe = context.vars.Int("qwe")
    qwe.set(int(time.time()))

    print(app.vars.var("qwe").get())
    print(context.vars.var("qwe").get())

    print(app.vars.get("qwe"))
    print(app.vars.getall())
    print(context.vars.get("qwe"))
    print(context.vars.getall())


if __name__ == "__main__":
    suanpan.run(app)
