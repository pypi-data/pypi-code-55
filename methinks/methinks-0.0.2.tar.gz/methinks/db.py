import os
import datetime
import xxhash
import json
from flask_sqlalchemy import SQLAlchemy

from methinks.utils import str_to_date
from methinks.config import get_default_conf


db = SQLAlchemy()


class Entry(db.Model):
    __tablename__ = 'entry'

    id = db.Column(db.Integer, primary_key=True)
    hexid = db.Column(db.String(16), unique=True, nullable=False, index=True)
    text = db.Column(db.Text(), nullable=False)
    date = db.Column(db.Date(), index=True, nullable=False)
    last_edited = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    misc = db.Column(db.JSON, nullable=True)

    def __init__(self, **data):
        if 'id' in data:
            raise AttributeError('id cannot be set')
        if 'hexid' in data:
            raise AttributeError('hexid cannot be set')
        self.text = data.pop('text')
        self.date = data.pop('date')
        if 'last_edited' in data:
            self.last_edited = data.pop('last_edited')
        assert type(self.date) is datetime.date
        self.misc = data

        self.hexid = self.hash

    def __repr__(self):
        return 'Entry: %r:\n%s' % (self.date, self.text)

    @property
    def hash(self):
        content = '%s%s%s' % (self.text, self.date, json.dumps(self.misc))
        hs = xxhash.xxh64(content).hexdigest()
        return hs

    @classmethod
    def string_to_date(cl, text):
        return datetime.datetime.strptime(text,
                                          get_default_conf()['dateformat']).date()

    @classmethod
    def date_to_string(cl, date):
        return date.strftime(get_default_conf()['dateformat'])

    @property
    def filename(self):
        return '%s.md' % Entry.date_to_string(self.date)

    def as_dict(self):
        d = dict(id=self.id,
                 hexid=self.hexid,
                 text=self.text,
                 date=self.date,
                 last_edited=self.last_edited,
                 **self.misc)
        return d

    @classmethod
    def from_dict(cl, data):
        return Entry(text=data['text'],
                     date=str_to_date(data['date']).date(),
                     last_edited=str_to_date(data['last_edited']),
                     **data.get('misc', {}))

    def to_file(self, folderpath):
        path = os.path.join(folderpath, self.filename)
        with open(path, 'w') as f:
            f.write(self.text)

    @classmethod
    def from_file(cl, filepath):
        with open(filepath, 'r') as f:
            contents = f.read()
        filename = os.path.basename(filepath).replace('.md', '')
        if filename == 'template':
            date = datetime.date.today()
            last_edited = datetime.datetime.min
        else:
            date = cl.string_to_date(filename)
            mtime = os.path.getmtime(filepath)
            last_edited = datetime.datetime.fromtimestamp(mtime)

        return Entry(text=contents, date=date, last_edited=last_edited)

    @classmethod
    def from_config(cl, config):
        sections = []
        for title, cl in config.triggers.items():
            line = cl.default_text(title)
            sections.append(line)
        contents = '%s\n' % '\n'.join(sections)
        date = datetime.date.today()
        last_edited = datetime.datetime.min

        return Entry(text=contents, date=date, last_edited=last_edited)
