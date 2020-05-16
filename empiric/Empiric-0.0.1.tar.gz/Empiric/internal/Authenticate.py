from flask import redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin

class Authenticate:
  @staticmethod
  def init(app, statisticsPassword):
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
        if 'password' in request.form and request.form['password'] == statisticsPassword:
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
