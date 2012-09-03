from flask.ext.sqlalchemy import SQLAlchemy
from dateutil import parser
import requests
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Numeric)
    lng = db.Column(db.Numeric)
    title = db.Column(db.String, unique=True)
    address = db.Column(db.Text)
    desc = db.Column(db.Text)
    link = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    featured = db.Column(db.Boolean)
    paid = db.Column(db.Boolean)
    popularity = db.Column(db.Integer)

    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    owner = db.relationship('Owner', backref=db.backref('events'), lazy='joined')

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), index=True)
    city = db.relationship('City', backref=db.backref('events'), lazy='joined')

    def __init__(self, address, title, owner, start_date, end_date, city, desc=None, link=None, featured=False, paid=False):
        self.address, self.lat, self.lng = _geocode(address)
        self.title = title
        self.owner = owner
        self.desc = desc
        self.link = link
        self.start_date = parser.parse(start_date, fuzzy=True)
        self.end_date = parser.parse(end_date, fuzzy=True)
        self.city = city
        self.paid = paid

        if type(featured) == str:
            self.featured = featured.lower() in ['true', 't', 'yes', 'y', '1']
        elif type(featured) == bool:
            self.featured = featured
        else:
            self.featured = False

    def __repr__(self):
        return '<Event %r>' % self.title

    def __str__(self):
        return self.title


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Owner %s>' % self.name

    def __str__(self):
        return self.name


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    lat = db.Column(db.Numeric)
    lng = db.Column(db.Numeric)

    def __init__(self, name):
        self.name = name
        address, self.lat, self.lng = _geocode(name)

    def __repr__(self):
        return '<City %s>' % self.name

    def __str__(self):
        return self.name


def add_item(item):
    try:
        db.session.add(item)
        db.session.commit()
        return
    except IntegrityError as e:
        db.session.rollback()
        return "Duplicate entry"
    except Exception as e:
        print e
        db.session.rollback()
        return repr(e)


def delete_item(item):
    try:
        db.session.delete(item)
        db.session.commit()
        return
    except Exception as e:
        print e
        db.session.rollback()
        return repr(e)


def _geocode(address):
    url = 'http://maps.googleapis.com/maps/api/geocode/json'
    payload = {'sensor': 'false', 'address': address}
    resp = requests.get(url, params=payload)
    result = resp.json['results'][0]
    address = result['formatted_address']
    lat = result['geometry']['location']['lat']
    lng = result['geometry']['location']['lng']

    return address, lat, lng
