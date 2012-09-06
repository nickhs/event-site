from flask import Flask
from models import db
from views import data_api, admin

app = Flask('eventsite')
app.config.from_pyfile('config.py')

app.register_blueprint(data_api)
app.register_blueprint(admin)

db.init_app(app)
