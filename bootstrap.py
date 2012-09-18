from eventsite import app, db
from eventsite.models import Owner, City, Event
import datetime
import random
import faker

addresses = [{'address': '989 Market Street', 'city': 'San Francisco', 'state': 'CA'},
             {'address': '1230 York Avenue', 'city': 'New York', 'state': 'NY'},
             {'address': '32 East 31st Street', 'city': 'New York', 'state': 'NY'},
             {'address': '291 Broadway', 'city': 'New York', 'state': 'NY'},
             {'address': '587 10th Avenue', 'city': 'New York', 'state': 'NY'},
             {'address': '2900 22nd Street', 'city': 'San Francisco', 'state': 'CA'},
             {'address': '77 De Boom Street', 'city': 'San Francisco', 'state': 'CA'},
             {'address': '149 9th Street', 'city': 'San Francisco', 'state': 'CA'},
             {'address': '733 Front Street', 'city': 'San Francisco', 'state': 'CA'},
             {'address': '842 Folsom Street', 'city': 'San Francisco', 'state': 'CA'}]


def get_start_time():
    return datetime.datetime.today() - datetime.timedelta(days=10)


def create_full_address(i):
    addr = addresses[i]
    return '%s, %s, %s' % (addr['address'], addr['city'], addr['state'])


def create_owner():
    owner = Owner()
    owner.name = faker.name.first_name().lower()
    owner.password = 'testpass'
    db.session.add(owner)
    db.session.commit()
    print owner.name
    return owner


def create_city(i):
    name = addresses[i]['city']
    city = City.query.filter_by(name=name).first()

    if city is None:
        city = City(name)
        db.session.add(city)
        db.session.commit()

    print city
    return city


def create_fake_event(i):
    """
    Creates a fake event for use in testing.
    """
    event = Event(address=create_full_address(i),
                  title=' '.join(faker.lorem.words()).title(),
                  owner=create_owner(),
                  desc=faker.lorem.paragraph(),
                  city=create_city(i),
                  start_date=str(faker.date.datetime(get_start_time())),
                  end_date=str(faker.date.datetime(get_start_time())
                               + datetime.timedelta(days=5)),
                  link='http://%s' % faker.internet.domain_name(),
                  featured=random.choice([True, False]),
                  paid=random.choice(['$10.00', '$20.00', '$200.00', 'Free']))

    db.session.add(event)
    db.session.commit()

if __name__ == '__main__':
    with app.test_request_context():
        db.drop_all()
        db.create_all()
        for i in xrange(len(addresses)):
            create_fake_event(i)
