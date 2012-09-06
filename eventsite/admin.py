from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView
from models import Event, db

admin = Admin(name='Event Site')

admin.add_view(ModelView(Event, db.session))
