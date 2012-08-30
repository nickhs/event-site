from app import *

db.drop_all()
db.create_all()

owner = Owner('arthur')
db.session.add(owner)
db.session.commit()

city = City('San Francisco')
db.session.add(city)
db.session.commit()

ev1 = Event(address='970 Folsom St, San Francisco, CA', 
            title='Super duper fun', 
            owner=owner, 
            desc='Who doesn\'t want to have fun?', 
            city=city,
            start_date='20 September 2012',
            end_date='22 September 2012',
            link='http://google.com/',
            featured=True)
db.session.add(ev1)
db.session.commit()
