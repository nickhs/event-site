from flask.ext.admin import Admin
from flask.ext.login import current_user
from flask.ext.admin.contrib.sqlamodel import ModelView
from models import Event, db

admin = Admin(name='Event Site')


class CustomView(ModelView):
    def is_accessible(self):
      return current_user.is_authenticated()

    list_columns = ('title', 'desc', 'address', 'start_date', 'end_date',
                    'city', 'featured', 'paid', 'owner', 'link')

    form_columns = list_columns

    rename_columns = dict(desc='Description')

    def create_model(self, form):
        model = Event(address=form.address.data,
                      title=form.title.data,
                      owner=form.owner.data,
                      city=form.city.data,
                      start_date=str(form.start_date.data),
                      end_date=str(form.end_date.data),
                      desc=form.desc.data,
                      link=form.link.data,
                      paid=form.paid.data,
                      featured=form.featured.data)
        self.session.add(model)
        self.session.commit()

    def __init__(self, session):
        super(CustomView, self).__init__(Event, session)

view = CustomView(db.session)
admin.add_view(view)
