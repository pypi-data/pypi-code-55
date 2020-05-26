"""
mblog: a minimal markdown blog
"""
# pylint: disable=W
# pylint: disable=missing-docstring

from __future__ import print_function
import base64
import datetime
import functools
import hashlib
import os
import re
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

try:
    from flask import (abort, Flask, flash, Markup, redirect,
                       render_template, request,
                       send_file, session, url_for)
    from markdown import markdown
    from markdown.extensions.codehilite import CodeHiliteExtension
    from markdown.extensions.extra import ExtraExtension
    from micawber import bootstrap_basic, parse_html
    from micawber.cache import Cache as OEmbedCache
    from peewee import (CharField, TextField, BooleanField,
                        DateTimeField, IntegrityError, SQL)
    from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
    from playhouse.sqlite_ext import FTSModel
    from werkzeug.utils import secure_filename
except ImportError:
    print("Dependencies aren't installed. Run: \n $ pip install -r requirements.txt")
    exit(1)

# Blog configuration values.
HOST = os.environ.get('HOST') or '0.0.0.0'
PORT = int(os.environ.get('PORT') or '5000')

# You may consider using a one-way hash to generate the password, and then
# use the hash again in the login view to perform the comparison. This is just
# for simplicity.
USER = os.environ.get('USER') or 'user'

# Default: base64(sha2('Password'))
ADMIN_PASSWORD_FILE=os.path.expanduser('~/.{}-blog.pass'.format(USER))
if os.path.exists(ADMIN_PASSWORD_FILE):
   ADMIN_PASSWORD_HASH= open(ADMIN_PASSWORD_FILE).read().strip()
else:
   ADMIN_PASSWORD_HASH = os.environ.get('PASSWORD_HASH') or \
   '588+9PF8OZmpTyxvYS6KiI5bECaHjk4ZOYsjvTjsIho='

APP_DIR = os.path.dirname(os.path.realpath(__file__))

# Default: ../README.md
APP_README_FILE = os.path.join(os.path.dirname(APP_DIR), 'README.md')
if os.path.exists(APP_README_FILE):
    APP_README = open(APP_README_FILE).read()
else:
    APP_README = 'Please see README.md'

# The playhouse.flask_utils.FlaskDB object accepts database URL configuration.
DATABASE_DIR = os.environ.get('DATABASE_DIR') or os.path.expanduser('~')
DATABASE = 'sqliteext:///%s' % os.path.join(
    DATABASE_DIR, '.{}-blog.db'.format(USER))

# This directory is where files are uploaded to.
UPLOAD_DIR = os.environ.get('UPLOAD_DIR') or\
    os.path.expanduser('~/.{}-blog-uploads'.format(USER))

# The secret key is used internally by Flask to encrypt session data stored
# in cookies. Make this unique for your app.
SECRET_KEY = os.environ.get('COOKIE_SECRET') or 'shhh, secret!'

# This is used by micawber, which will attempt to generate rich media
# embedded objects with maxwidth=800.
SITE_WIDTH = 400

# Debug parameters
DEBUG = False

# Create a Flask WSGI app and configure it using values from the module.
app = Flask(__name__)
app.config.from_object(__name__)

# FlaskDB is a wrapper for a peewee database that sets up pre/post-request
# hooks for managing database connections.
flask_db = FlaskDB(app)

# The `database` is the actual peewee database, as opposed to flask_db which is the wrapper.
database = flask_db.database

# Configure micawber with the default OEmbed providers (YouTube, Flickr, etc).
# We'll use a simple in-memory cache so that multiple requests for the same
# video don't require multiple network requests.
oembed_providers = bootstrap_basic(OEmbedCache())


class Entry(flask_db.Model):
    title = CharField()
    slug = CharField(unique=True)
    content = TextField()
    published = BooleanField(index=True)
    timestamp = DateTimeField(default=datetime.datetime.now, index=True)

    @property
    def html_content(self):
        """
        Generate HTML representation of the markdown-formatted blog entry,
        and also convert any media URLs into rich media objects such as video
        players or images.
        """
        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        markdown_content = markdown(self.content, extensions=[hilite, extras])
        oembed_content = parse_html(
            markdown_content,
            oembed_providers,
            urlize_all=True,
            maxwidth=app.config['SITE_WIDTH'])
        return Markup(oembed_content)

    def save(self, *args, **kwargs):
        # Generate a URL-friendly representation of the entry's title.
        if not self.slug:
            self.slug = re.sub(r'[^\w]+', '-', self.title.lower()).strip('-')
        ret = super(Entry, self).save(*args, **kwargs)

        # Store search content.
        self.update_search_index()
        return ret

    def update_search_index(self):
        # Create a row in the FTSEntry table with the post content. This will
        # allow us to use SQLite's awesome full-text search extension to
        # search our entries.
        exists = (FTSEntry
                  .select(FTSEntry.docid)
                  .where(FTSEntry.docid == self.id)
                  .exists())
        content = '\n'.join((self.title, self.content))
        if exists:
            (FTSEntry
             .update({FTSEntry.content: content})
             .where(FTSEntry.docid == self.id)
             .execute())
        else:
            FTSEntry.insert({
                FTSEntry.docid: self.id,
                FTSEntry.content: content}).execute()

    @classmethod
    def public(cls):
        return Entry.select().where(Entry.published)

    @classmethod
    def drafts(cls):
        return Entry.select().where(not Entry.published)

    @classmethod
    def search(cls, query):
        words = [word.strip() for word in query.split() if word.strip()]
        if not words:
            # Return an empty query.
            return Entry.noop()
        else:
            search = ' '.join(words)

        # Query the full-text search index for entries matching the given
        # search query, then join the actual Entry data on the matching
        # search result.
        return (Entry
                .select(Entry, FTSEntry.rank().alias('score'))
                .join(FTSEntry, on=(Entry.id == FTSEntry.docid))
                .where(
                    FTSEntry.match(search) &
                    Entry.published)
                .order_by(SQL('score')))


class FTSEntry(FTSModel):
    content = TextField()

    class Meta(object):
        database = database


def login_required(function):
    @functools.wraps(function)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return function(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return inner


@app.route('/login/', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('password'):
        password = request.form.get('password')
        # TODO: If using a one-way hash, you would also hash the
        # user-submitted password and do the comparison on the
        # hashed versions.
        hashed = base64.b64encode(hashlib.sha256(password.encode()).digest()).decode()
        if hashed == app.config['ADMIN_PASSWORD_HASH']:
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('login.html', next_url=next_url, user=USER)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return render_template('logout.html', user=USER)


@app.route('/')
def index():
    search_query = request.args.get('q')
    if search_query:
        query = Entry.search(search_query)
    else:
        query = Entry.public().order_by(Entry.timestamp.desc())

    # The `object_list` helper will take a base query and then handle
    # paginating the results if there are more than 20. For more info see
    # the docs:
    # http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#object_list
    return object_list(
        'index.html',
        query,
        search=search_query,
        check_bounds=False,
        user=USER)


def _delete(entry, template):
    try:
        with database.atomic():
            entry.delete_instance(recursive=True)
    except:
        flash('Error: Unable to delete entry.', 'danger')
    else:
        flash('Entry deleted successfully.', 'success')
    return render_template(template, entry=entry, user=USER)


def _create_or_edit(entry, template):
    if request.method == 'POST':
        entry.title = request.form.get('title') or ''
        entry.content = request.form.get('content') or ''
        entry.published = request.form.get('published') or False
        if not (entry.title and entry.content):
            flash('Title and Content are required.', 'danger')
        else:
            # Wrap the call to save in a transaction so we can roll it back
            # cleanly in the event of an integrity error.
            try:
                with database.atomic():
                    entry.save()
            except IntegrityError:
                flash('Error: this title is already in use.', 'danger')
            else:
                flash('Entry saved successfully.', 'success')
                if entry.published:
                    return redirect(url_for('detail', slug=entry.slug))
                return redirect(url_for('edit', slug=entry.slug))

    return render_template(template, entry=entry, user=USER)


def _upload(template):
    if request.method == 'POST':
        try:
            file_uploaded = request.files.get('file')
            if not file_uploaded:
                flash('You did not upload a file. Please try again.', 'danger')
            else:
                filename = secure_filename(file_uploaded.filename)
                filepath = os.path.join(UPLOAD_DIR, filename)
                if not os.path.exists(UPLOAD_DIR):
                    os.makedirs(UPLOAD_DIR)
                file_uploaded.save(filepath)
                fileurl = url_for('files', filename=filename)
                flash(
                    'File saved successfully as'
                    ' <a href="{}">{}</a>.'.format(fileurl, filename), 'success')
        except:
            flash('Unable to save file. Please try again.', 'danger')

    return render_template(template, user=USER)


@app.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    return _upload('upload.html')


@app.route('/files/<filename>')
def files(filename):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        abort(404)
    return send_file(filepath)


@app.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    return _create_or_edit(Entry(title='', content=''), 'create.html')


@app.route('/drafts/')
@login_required
def drafts():
    query = Entry.drafts().order_by(Entry.timestamp.desc())
    return object_list('index.html', query, check_bounds=False, user=USER)


@app.route('/<slug>/')
def detail(slug):
    if session.get('logged_in'):
        query = Entry.select()
    else:
        query = Entry.public()
    if slug == 'README':
        entry = Entry(title='README', content=APP_README, slug=slug)
    else:
        entry = get_object_or_404(query, Entry.slug == slug)
    return render_template('detail.html', entry=entry, user=USER)


@app.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    entry = get_object_or_404(Entry, Entry.slug == slug)
    return _create_or_edit(entry, 'edit.html')


@app.route('/<slug>/delete/', methods=['GET'])
@login_required
def delete(slug):
    entry = get_object_or_404(Entry, Entry.slug == slug)
    return _delete(entry, 'delete.html')


@app.template_filter('clean_querystring')
def clean_querystring(request_args, *keys_to_remove, **new_values):
    # We'll use this template filter in the pagination include. This filter
    # will take the current URL and allow us to preserve the arguments in the
    # querystring while replacing any that we need to overwrite. For instance
    # if your URL is /?q=search+query&page=2 and we want to preserve the search
    # term but make a link to page 3, this filter will allow us to do that.
    querystring = dict((key, value)
                       for key, value in list(request_args.items()))
    for key in keys_to_remove:
        querystring.pop(key, None)
    querystring.update(new_values)
    return urlencode(querystring)


@app.errorhandler(404)
def not_found(exc):
    return render_template('notfound.html', user=USER), 404


@app.errorhandler(500)
def error(exc):
    return render_template('error.html', user=USER), 500


def start_blog():
    database.create_tables([Entry, FTSEntry], safe=True)
    app.run(debug=DEBUG, host=HOST, port=PORT)
