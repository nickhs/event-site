from flask import Flask
from models import db
from admin import admin
from views import data_api

app = Flask('eventsite')
app.config.from_pyfile('config.py')

app.register_blueprint(data_api)

db.init_app(app)
admin.init_app(app)
