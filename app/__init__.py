import datetime
from cgi import logfile
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment


app = Flask(__name__)
app.config.from_object('config')
app.config["SECRET_KEY"] = "88HBDJ772AS"
db = SQLAlchemy(app)
moment = Moment(app)
admin = Admin(app, template_mode='bootstrap3')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "app.login"
login_manager.session_protection = "strong"


# logger = logging.getLogger()
# handler = logging.handlers.TimedRotatingFileHandler(logfile, 'S', 1, 0)
# handler.suffix = '%Y%m%d'
# logger.addHandler(handler)
# logger.fatal(datetime.datetime.now().strftime('%Y-%m-%d'))


app.debug = True
handler = logging.FileHandler('flask.log', encoding='UTF-8')
handler.setLevel(logging.DEBUG)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)


from app import models, views
