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

    city = City('New York')
    db.session.add(city)
    db.session.commit()

    ev3 = Event(address='DBGB Kitchen and Bar, 299 Bowery St, NY',
                owner=owner,
                city=city,
                title='New York Event',
                start_date='31 Aug',
                end_date='2 Sept')

    ev4 = Event(address='Murray\'s Bagels, 500 6th Ave, NY',
                owner=owner,
                city=city,
                title='New York Event 2',
                start_date='4 Sept',
                end_date='10 Sept')

    db.session.add(ev3)
    db.session.add(ev4)
    db.session.commit()
