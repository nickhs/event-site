from eventsite import app, db
from eventsite.models import Owner, City, Event
import datetime
import random
import faker

addresses = [{'address': '565 Angel Bernal, 15324 Rancho Serena Dr', 'city': 'Paramount', 'state': 'CA', 'zip': '90723-4579'},
             {'address': '4106 Tucson Dr', 'city': 'Greensboro', 'state': 'NC', 'zip': '27406-6333'},
             {'address': '500 E Sixth St, Apt 2', 'city': 'Prairie City', 'state': 'IA', 'zip': '50228-8608'},
             {'address': '2600 Pine Lake Dr', 'city': 'Greensboro', 'state': 'NC', 'zip': '27407-6646'},
             {'address': '5302 Texoma Pkwy', 'city': 'Sherman', 'state': 'TX', 'zip': '75090-2112'},
             {'address': '1318 N Vasco Rd', 'city': 'Livermore', 'state': 'CA', 'zip': '94551-9212'},
             {'address': '1700 W New Haven Ave', 'city': 'Melbourne', 'state': 'FL', 'zip': '32904-3919'},
             {'address': '16900 N Bay Rd', 'city': 'Sunny Isles Beach', 'state': 'FL', 'zip': '33160-4252'},
             {'address': '410 Gardenia Ln', 'city': 'Buffalo Grove', 'state': 'IL', 'zip': '60089-1661'},
             {'address': '1511 E 86th St', 'city': 'Chicago', 'state': 'IL', 'zip': '60619-6518'}]


def get_start_time():
    return datetime.datetime.today() - datetime.timedelta(days=10)


def create_full_address(i):
    addr = addresses[i]
    return '%s, %s, %s, %s' % (addr['address'], addr['city'], addr['state'], addr['zip'])


def create_owner():
    owner = Owner(faker.name.name())
    db.session.add(owner)
    db.session.commit()
    return owner


def create_city(i):
    city = City(addresses[i]['city'])
    print city
    db.session.add(city)
    db.session.commit()
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
                  featured=random.choice([True, False]))

    db.session.add(event)
    db.session.commit()

if __name__ == '__main__':
    with app.test_request_context():
        db.drop_all()
        db.create_all()
        for i in xrange(len(addresses)):
            create_fake_event(i)
