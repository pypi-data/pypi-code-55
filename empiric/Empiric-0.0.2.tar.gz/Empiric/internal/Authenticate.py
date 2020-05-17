from flask import redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin

from Empiric.internal.Print import Print

class Authenticate:
  @staticmethod
  def _validPassword(password):
    return password is not None and len(password) > 5
  @staticmethod
  def init(app, password):
    if password is None:
      Print.log('No password for the statistics website provided. The')
      Print.log2('page will be disabled.')
    elif not Authenticate._validPassword(password):
      Print.logWarning('The password for the statistics websites needs to be')
      Print.log2Warning('six characters in length at the minimum. The page will')
      Print.log2Warning('be disabled.')
    app.config.update(SECRET_KEY='Empiric!', USE_SESSION_FOR_NEXT=True)
    loginManager = LoginManager()
    loginManager.init_app(app)
    loginManager.login_view = 'login'
    defaultUser = 'statistics'
    class User(UserMixin):
      def __init__(self, username):
        self.id = username
      def __repr__(self):
        return self.username
    @app.route('/login', methods=['GET', 'POST'])
    def login():
      if request.method == 'POST':
        if 'password' in request.form and Authenticate._validPassword(password) and request.form['password'] == password:
          login_user(User(defaultUser))
          return redirect(url_for('statistics'))
        else:
          return render_template('login.html', message='Wrong password. Please try again.')
      elif request.method == 'GET':
        return render_template('login.html')
      return render_template('login.html', message='Bad login request.')
    @app.route('/logout')
    @login_required
    def logout():
      logout_user()
      return redirect(url_for('login'))
    @loginManager.user_loader
    def loader_user(username):
      return User(username)
