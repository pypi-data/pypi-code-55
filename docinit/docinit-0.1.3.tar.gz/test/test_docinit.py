import os
import pytest
from datetime import datetime
from docinit.docinit import Parse, Config, Git

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'setup.cfg')

def test_parse_bool():
    assert Parse.option('tRUe') == True
    assert Parse.option('1') == True
    assert Parse.option('yEs') == True
    assert Parse.option('FalSE') == False
    assert Parse.option('0') == False
    assert Parse.option('No') == False

def test_parse_int():
    assert Parse.option('42') == 42

def test_parse_float():
    assert Parse.option('1.337') == 1.337

def test_parse_none():
    assert Parse.option('noNe') == None

def test_parse_list():
    assert Parse.option('trUE,42,    7.8, hello, none') == [True, 42, 7.8, 'hello', None]
    assert Parse.option('\n42 \n    hello') == [42, 'hello']

def test_parse_dict():
    assert Parse.option('\nfoo=bar\nbaz = 42') == {'foo': 'bar', 'baz': 42}
    assert Parse.option('a=b,b=yes') == {'a': 'b', 'b': True}

def test_config_default():
    config = Config(path).config['docinit']
    assert config['doc_dir'] == 'doc'
    assert config['name'] == 'docinit'
    assert config['parent_url'] == None

def test_config_doc_dir():
    config = Config(path)
    assert config.config['docinit']['doc_dir'] == 'doc'
    config.config['build_sphinx']['source-dir'] = 'foo'
    config._set_doc_dir()
    assert config.config['docinit']['doc_dir'] == 'foo'

def test_config_name():
    config = Config(path)
    assert config.config['docinit']['name'] == 'docinit'
    config.config['metadata']['name'] = 'Foo'
    config._set_name()
    assert config.config['docinit']['name'] == 'Foo'
    config.config['build_sphinx']['project'] = 'Bar'
    config._set_name()
    assert config.config['docinit']['name'] == 'Bar'

def test_config_version():
    config = Config(path)
    config.config['metadata']['version'] = '42.0.0'
    config._set_version()
    assert config.config['docinit']['version'] == '42.0.0'

def test_config_author():
    config = Config(path)
    assert config.config['docinit']['author'] == 'mesca'
    config.config['metadata']['author'] = 'Me'
    config._set_author()
    assert config.config['docinit']['author'] == 'Me'

def test_config_packages():
    config = Config(path)
    config.config['options']['packages'] = ['foo']
    config._set_packages()
    assert config.config['docinit']['packages'] == ['foo']

def test_config_copyright():
    year = str(datetime.now().year)
    config = Config(path)
    assert config.config['docinit']['copyright'].startswith('2020')
    config.config['git']['year'] = '2000'
    config._set_copyright()
    assert config.config['docinit']['copyright'] == f'2000-{year}, mesca'
    config.config['git']['year'] = year
    config._set_copyright()
    assert config.config['docinit']['copyright'] == f'{year}, mesca'
    config.config['build_sphinx']['copyright'] = 'foobar'
    config._set_copyright()
    assert config.config['docinit']['copyright'] == 'foobar'

def test_git():
    info = Git().info
    assert info['name'] == 'docinit'
    assert info['year'] == '2020'
