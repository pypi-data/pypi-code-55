import os
from jinja2 import Template


def get_dependencies():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    dependencies_path = "{}/templates/dependencies.html".format(current_dir)
    static_dir = "{}/static/".format(current_dir)

    with open(dependencies_path, 'r') as f:
        data = f.read()
    with open('{}tabs/tabs.css'.format(static_dir), 'r') as f:
        tabs_css = f.read()
    with open('{}editor/view-quill.css'.format(static_dir), 'r') as f:
        view_quill_css = f.read()
    with open('{}tabs/tabs.js'.format(static_dir), 'r') as f:
        tabs_js = f.read()
    with open('{}editor/editor.js'.format(static_dir), 'r') as f:
        editor_js = f.read()

    tm = Template(data)
    msg = tm.render(tabsCSS=tabs_css,
                    tabsJS=tabs_js,
                    editorJS=editor_js,
                    viewQuillCSS=view_quill_css,
                    quill_version='1.3.7')

    return msg
