from eventsite import app, db
from eventsite.models import Owner, City, Event
import datetime
import random
import faker

addresses = ['565 Angel Bernal, 15324 Rancho Serena Dr, Paramount, CA 90723-4579',
'4106 Tucson Dr, Greensboro, NC 27406-6333',
'500 E Sixth St, Apt 2, Prairie City, IA 50228-8608',
'2600 Pine Lake Dr, Greensboro, NC 27407-6646',
'5302 Texoma Pkwy, Sherman, TX 75090-2112',
'886 Bay Ridge Ave, Brooklyn, NY 11220-5710',
'1318 N Vasco Rd, Livermore, CA 94551-9212',
'1700 W New Haven Ave, Melbourne, FL 32904-3919',
'16900 N Bay Rd, Sunny Isles Beach, FL 33160-4252',
'410 Gardenia Ln, Buffalo Grove, IL 60089-1661',
'1511 E 86th St, Chicago, IL 60619-6518',
'28 Milford St, Medway, MA 02053-1631',
'9402 Bentridge Ave, Potomac, MD 20854-2870',
'1018 Adams Ave, Apt 3C, Salisbury, MD 21804-6687',
'1901 Kylemore Dr, Greensboro, NC 27406-6440',
'201 Railroad Ave, East Rutherford, NJ 07073-1943',
'3333 228th St SE, Bothell, WA 98021-8950',
'4510 W Capitol Dr, Milwaukee, WI 53216-1564',
'1803 S Eighth St, Rogers, AR 72756-5912',
'1812 Chartwell Dr, Fort Wayne, IN 46816-1382']

def get_start_time():
    return datetime.datetime.today() - datetime.timedelta(days=10)

def create_full_address():
    street = faker.address.street_address(include_secondary=True)
    city = faker.address.city()
    state = faker.address.us_state_abbr()
    print '%s, %s, %s' % (street, city, state)
    return '%s, %s, %s' % (street, city, state)

def create_owner():
    owner = Owner(faker.name.name())
    db.session.add(owner)
    db.session.commit()
    return owner

def create_city():
    city = City(faker.address.city())
    db.session.add(city)
    db.session.commit()
    return city

def create_fake_event(i):
    """
    Creates a fake event for use in testing.
    """
    event = Event(address=addresses[i],
                title=' '.join(faker.lorem.words()).title(),
                owner=create_owner(),
                desc=faker.lorem.paragraph(),
                city=create_city(),
                start_date=str(faker.date.datetime(get_start_time())),
                end_date=str(faker.date.datetime(get_start_time()) \
                            + datetime.timedelta(days=5)),
                link='http://%s' % faker.internet.domain_name(),
                featured=random.choice([True, False]))

    db.session.add(event)
    db.session.commit()

if __name__ == '__main__':
    with app.test_request_context():
        db.drop_all()
        db.create_all()
        for i in xrange(20): create_fake_event(i)

