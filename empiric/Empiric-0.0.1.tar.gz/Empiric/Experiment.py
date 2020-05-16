from flask import Flask, jsonify, redirect, render_template, request
from flask_login import login_required
import os
import shutil
import sys
import subprocess
import threading
import webbrowser

from Empiric import pkgName, pkgVersion, pkgUrl
from Empiric.internal.AccessCodes import AccessCodes
from Empiric.internal.Authenticate import Authenticate
from Empiric.internal.ManuscriptMemory import ManuscriptMemories, StepNeedsToBeRun
from Empiric.internal.Print import COLORS, Print
from Empiric.internal.Statistics import Statistics
from Empiric.Mode import MODE
from Empiric.Pages.PageAccessCode import pageAccessCode
from Empiric.Pages.PageFinal import pageFinal

class Experiment:
  _pathStaticFile = 'files'
  def __init__(self):
    self._ms = ManuscriptMemories()
    self._info()
  def _computePath(self, path, pathname):
    return path if path else os.path.join(os.path.dirname(sys.argv[0]), pathname)
  def _info(self):
    width = 54
    Print.log2()
    Print.log2('=' * width)
    Print.log2('== ', f'{pkgName} v{pkgVersion}', ' ' * (width - 8 - len(pkgName) - len(pkgVersion)), ' ==')
    Print.log2('== ', pkgUrl, ' ' * (width - 6 - len(pkgUrl)), ' ==')
    Print.log2('=' * width)
    Print.log2()
  def _yarnCheck(self):
    try:
      Print.log('Checking for Yarn')
      subprocess.run(['yarn', '--version'], capture_output=True)
      Print.log2('Found')
    except:
      Print.log2()
      Print.log2(f'{COLORS.ERROR}ERROR: Yarn is needed. Please install it.')
      Print.log2()
      Print.log2('You find Yarn here:  https://yarnpkg.com')
      Print.log2()
      Print.log2('Yarn is required to download libraries needed for the')
      Print.log2(f'web interface.{COLORS.DEFAULT}')
      Print.log2()
      return False
    return True
  def _yarnCopyPackageFiles(self, pathStatic):
    try:
      if not os.path.exists(pathStatic):
        Print.log('Creating path for static data')
        os.makedirs(pathStatic)
        Print.log2('Success')
      Print.log('Copy files to the path for static data')
      for filename in ['package.json', 'yarn.lock', '.yarnrc']:
        shutil.copy(os.path.join(os.path.dirname(__file__), '..', 'files', filename), os.path.join(pathStatic, filename))
      Print.log2('Success')
    except:
      Print.log2()
      Print.log2(f'{COLORS.ERROR}ERROR: Could not copy Yarn package files.{COLORS.DEFAULT}')
      Print.log2()
      return False
    return True
  def _yarnInstall(self, pathStatic):
    try:
      Print.log('Installing JavaScript libraries using yarn')
      subprocess.run(['yarn', 'install'], capture_output=True, cwd=pathStatic)
      Print.log2('Success')
    except:
      Print.log2()
      Print.log2(f'{COLORS.ERROR}ERROR: Yarn could not install the libraries needed.')
      Print.log2()
      Print.log2('Please run yarn on your own:')
      Print.log2(f'> cd static && yarn install{COLORS.DEFAULT}')
      Print.log2()
      return False
    return True
  def _createPathStaticFile(self, pathStatic):
    try:
      p = os.path.join(pathStatic, Experiment._pathStaticFile)
      if not os.path.exists(p):
        Print.log('Creating path for static files')
        os.makedirs(p)
        Print.log2('Success')
    except:
      Print.log2()
      Print.log2(f'{COLORS.ERROR}ERROR: Could not create path for static files.{COLORS.DEFAULT}')
      Print.log2()
      return False
    return True
  def createPageStructure(self):
    pathRoot = self._computePath(None, '')
    pathPages = self._computePath(None, 'pages')
    pathPagesInit = os.path.join(pathPages, '__init__.py')
    pathTemplates = self._computePath(None, 'templates')
    if not os.path.exists(pathPages):
      Print.log('Creating path for pages')
      os.makedirs(pathPages)
      Print.log2('Success')
    if not os.path.exists(pathPagesInit):
      Print.log('Creating init file for the path for pages')
      with open(pathPagesInit, 'a'):
        pass
      Print.log2('Success')
    if not os.path.exists(pathTemplates):
      Print.log('Creating path for templates')
      os.makedirs(pathTemplates)
      Print.log2('Success')
    Print.log('Copy example files')
    for p, filename in [(pathPages, '_PageExample.py'), (pathTemplates, '_pageExample.html')]:
      if not os.path.exists(os.path.join(p, filename)):
        shutil.copy(os.path.join(os.path.dirname(__file__), '..', 'files', filename), os.path.join(p, filename))
    for filenameSrc, filenameDst in [('.yarnrc2', '.yarnrc'), ('package2.json', 'package.json')]:
      if not os.path.exists(os.path.join(pathRoot, filenameDst)):
        shutil.copy(os.path.join(os.path.dirname(__file__), '..', 'files', filenameSrc), os.path.join(pathRoot, filenameDst))
    Print.log2('Success')
  def run(self, manuscript, port=5000, debug=False, openBrowser=True, pathStatic=None, pathTemplates=None, mode=MODE.LOCAL, numberOfAccessCodes=1000, statistics=False, statisticsPassword=None):
    self._port = port
    self._debug = debug
    self._openBrowser = openBrowser
    self._pathStatic = self._computePath(pathStatic, 'static')
    self._pathTemplates = self._computePath(pathTemplates, 'templates')
    self._mode = mode
    self._statistics = statistics
    self._statisticsPassword = statisticsPassword
    self._readyToStart = self._yarnCheck() and self._yarnCopyPackageFiles(self._pathStatic) and self._yarnInstall(self._pathStatic) and self._createPathStaticFile(self._pathStatic)
    if not self._readyToStart:
      return
    self._ac = AccessCodes(self._mode, numberOfAccessCodes)
    app = Flask(__name__, static_folder=self._pathStatic)
    app.jinja_loader.searchpath.append(self._pathTemplates)
    Authenticate.init(app, self._statisticsPassword)
    @app.route('/')
    def base():
      if self._mode == MODE.LOCAL:
        return redirect('/' + AccessCodes.defaultAccessCode())
      elif self._mode == MODE.USE_ACCESS_CODES:
        return pageAccessCode(None)
      elif self._mode == MODE.NO_ACCESS_CODES:
        return redirect('/' + AccessCodes.newAccessCode())
    @app.route('/<string:accessCode>')
    def step(accessCode):
      if not self._ac.exists(accessCode):
        return pageAccessCode(None, showErrorMessage=True)
      m = self._ms.get(accessCode)
      m.prepareRun()
      try:
        manuscript(m)
        pageFinal(m)
      except StepNeedsToBeRun as e:
        return render_template(e.page().template(), accessCode=m.accessCode(), step=e.step())
    @app.route('/save/<string:accessCode>/<int:step>', methods=['POST'])
    def save(accessCode, step):
      if not self._ac.exists(accessCode):
        return jsonify({'success': False})
      self._ms.get(accessCode).save(step, request.get_json())
      return jsonify({'success': True})
    @app.route('/settings/<string:accessCode>/<int:step>')
    def settings(accessCode, step):
      if not self._ac.exists(accessCode):
        return jsonify({'success': False})
      return jsonify(self._ms.get(accessCode).settings(step))
    @app.route('/statistics')
    @login_required
    def statistics():
      return render_template('statistics.html')
    @app.route('/data/statistics.json')
    @login_required
    def dataStatistics():
      data = Statistics().statisticsData()
      return jsonify(data)
    if self._openBrowser:
      threading.Timer(1, lambda: webbrowser.open(f'http://127.0.0.1:{self._port}')).start()
    app.run(port=self._port, debug=self._debug)
