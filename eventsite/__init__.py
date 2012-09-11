from flask import Flask
from login import login_manager, auth
from models import db
from admin import admin
from views import data_api

app = Flask('eventsite')
app.config.from_pyfile('config.py')

app.register_blueprint(data_api)
app.register_blueprint(auth)

db.init_app(app)
admin.init_app(app)
login_manager.init_app(app)
