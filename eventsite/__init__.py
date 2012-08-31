from flask import Flask
from models import db
from views import data_api
import config


app = Flask('eventsite')
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY
app.host = config.HOST
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

app.register_blueprint(data_api)

db.init_app(app)
