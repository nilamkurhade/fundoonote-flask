from flask_login import LoginManager
from fundooapp.views import *

app.secret_key = 'xxxxyyyyyzzzzz'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
