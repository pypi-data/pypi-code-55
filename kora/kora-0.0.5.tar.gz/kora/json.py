from requests import models
import json
from IPython.display import HTML

render_template = """
<script src="https://rawgit.com/caldwell/renderjson/master/renderjson.js"></script>
<script>
renderjson.set_show_to_level(1)
document.body.appendChild(renderjson(%s))
new ResizeObserver(google.colab.output.resizeIframeToContent).observe(document.body)
</script>
"""
models.Response._repr_html_ = lambda rsp: render_template % rsp.text

def render(jstr):
    if type(jstr) != str:
        jstr = json.dumps(jstr)
    return HTML(render_template % jstr)