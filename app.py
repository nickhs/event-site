from flask import Flask, render_template, jsonify, request
import requests
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from dateutil import parser
import simplejson as json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

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
        self.address = address
        self.__geocode__()
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

    def __geocode__(self):
        url = 'http://maps.googleapis.com/maps/api/geocode/json'
        payload = {'sensor': 'false', 'address': self.address}
        resp = requests.get(url, params=payload)
        result = resp.json['results'][0]
        self.address = result['formatted_address']
        self.lat = result['geometry']['location']['lat']
        self.lng = result['geometry']['location']['lng']


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

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<City %s>' % self.name

    def __str__(self):
        return self.name


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST', 'DELETE'])
def give_data():
    if request.method == 'GET':
        resp = handle_get(request)
        return jsonify(resp)

    elif request.method == 'POST':
        resp = handle_post(request)
        return jsonify(resp)
      
    elif request.method == 'DELETE':
        resp = handle_delete(request)
        return jsonify(resp)


def handle_get(request):
    if 'city' in request.args:
        to_find = request.args['city']
        city = City.query.filter_by(name=to_find).first()

        if city is None:
            items = []
        else:
            items = Event.query.filter_by(city_id=city.id).order_by(Event.start_date).limit(1).all()
    else:
        items = [convert_to_dict(x) for x in Event.query.limit(10).all()]

    return {'count': len(items), 'items': items}


def handle_post(request):
    data = request.json
        
    try:
        owner = Owner.query.filter_by(name=data['owner']).first()
        if owner is None:
            add_item(Owner(data['owner']))

        city = City.query.filter_by(name=data['city']).first()
        if city is None:
            add_item(City(data['city']))


        event = Event(address=data['address'],
                      title=data['title'],
                      start_date=data['start_date'],
                      end_date=data['end_date'],
                      owner=owner,
                      city=city,
                      desc=data.get('desc'),
                      link=data.get('link'),
                      featured=data.get('featured'),
                      paid=data.get('paid'))
        error = add_item(event)

        if (error != None):
            return {'status': 'IntegrityError', 'error': error}
    
    except KeyError as e:
        return {'status': 'KeyError failure', 'error': repr(e)}
    except Exception as e:
        return {'status': 'Unknown failure', 'error': repr(e)}
    
    return {'status': 'saved', 'event': convert_to_dict(event)}


def handle_delete(request):
    data = request.json
    event = None

    if 'id' in data:
        event = Event.query.get(data['id'])

    elif 'title' in data:
        event = Event.query.filter_by(title=data['title']).first()

    else:
        return {'status': 'failed', 'error': "No valid search specified. Valid search fields are id or name"};

    if event == None:
        return {'status': 'failed', 'error': 'No event found'}

    delete_item(event)
    return {'status': 'success', 'event': convert_to_dict(event)}



@app.route('/featured', methods=['GET'])
def give_better_data():
        events = Event.query.filter_by(featured=True).all()
        items = [convert_to_dict(x) for x in events]
        payload = {'count': len(items), 'items': items}
        return jsonify(payload)


@app.route('/owner', methods=['GET'])
def give_owners():
    items = [convert_to_dict(x) for x in Owner.query.all()]
    payload = {'count': len(items), 'items': items}
    return jsonify(payload)


def convert_to_dict(obj):
    ret = {}
    for key, val in obj.__dict__.items():
        if key.startswith('_'):
            continue

        ret[key] = str(val)

    return ret


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
    except Exception as e:
        print e
        db.session.rollback()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
