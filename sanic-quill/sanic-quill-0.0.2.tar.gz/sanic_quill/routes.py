from sanic import Blueprint
from sanic.response import text
import os
import html
from jinja2 import FileSystemLoader
from sanic_jinja2 import SanicJinja2
from sanic_quill.template import get_dependencies
from sanic_quill.form import EditForm

editor = Blueprint('editor')

loader = FileSystemLoader(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
)

jinja = SanicJinja2(loader=loader)


class cfg:
    get_data = None
    save_data = None
    img_folder = './img'
    route_for_img = '/img'


@editor.route('/uploaded_editor_files/', methods=('POST',))
async def uploaded_editor_files(request):
    # TODO: save your image and return url
    image = request.files['image'][0]
    if image:
        name = html.escape(image.name, True).replace(' ', '_')
        os.makedirs(cfg.img_folder, exist_ok=True)

        img_path = os.path.join(cfg.img_folder, name)
        with open(img_path, 'wb+') as destination:
            destination.write(image.body)
        img_url = f'{cfg.route_for_img}/{name}'
        return text(img_url)
    return request.form.image.data


@editor.route('/delete_file_by_url/', methods=('DELETE',))
async def delete_files(request):
    # TODO: save your image and return url
    return 'Image was deleted'
    

@editor.route('/edit', methods=['GET', 'POST'])
async def edit_route(request):
    params = dict(request.query_args)
    _id = params['id']
    data = cfg.get_data(_id)
    data = {
        'active': True,
        'tabs': [
            data
        ]}
    form = EditForm(data=data)
    if request.method == "POST":
        form.process(request.form)
        if form.validate():
            for tab in form.tabs:
                cfg.save_data(_id, tab.data)
    return jinja.render(
        'edit.html',
        request,
        form=form,
        sanic_quill_deps=get_dependencies(),
    )


def add_editor(app, get_data, save_data, img_folder=None, route_for_img='/img'):

    cfg.get_data = get_data
    cfg.save_data = save_data
    if img_folder:
        cfg.img_folder = img_folder
    cfg.route_for_img = route_for_img
    editor.static(cfg.route_for_img, cfg.img_folder)
    app.blueprint(editor)
