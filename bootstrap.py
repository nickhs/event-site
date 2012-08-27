from app import *

db.drop_all()
db.create_all()

owner = Owner('arthur')
db.session.add(owner)
db.session.commit()

ev1 = Event('970 Folsom St, San Francisco, CA', 'Super duper fun', owner, desc='Who doesn\'t want to have fun?', link='http://kiip.me/')
db.session.add(ev1)
db.session.commit()
