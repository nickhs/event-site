from eventsite import app, db
from eventsite.models import City, Event, Owner

with app.test_request_context():
    db.drop_all()
    db.create_all()

    city = City('San Francisco')
    db.session.add(city)
    db.session.commit()

    owner = Owner('Nick')
    db.session.add(owner)
    db.session.commit()

    ev1 = Event(address='751 Commercial St, San Francsico, CA',
                owner=owner,
                city=city,
                title='Awesome Event',
                start_date='31 Aug',
                end_date='1 September')

    ev2 = Event(address='970 Folsom St, San Francsico, CA',
                owner=owner,
                city=city,
                title='Awesome Event2',
                start_date='30 Nov',
                end_date='10 Dec')

    db.session.add(ev1)
    db.session.add(ev2)
    db.session.commit()
