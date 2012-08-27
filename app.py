from flask import Flask, render_template, jsonify, request, Response
import requests
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import simplejson as json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Numeric)
    lng = db.Column(db.Numeric)
    title = db.Column(db.String(100), unique=True)
    address = db.Column(db.Text)
    desc = db.Column(db.Text)
    link = db.Column(db.String(100))
    date = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    owner = db.relationship('Owner', backref=db.backref('events', lazy='dynamic'))

    def __init__(self, address, title, owner, desc=None, link=None, date=datetime.utcnow()):
        self.address = address # FIXME geocoding
        self.__geocode__()
        self.title = title
        self.owner = owner
        self.desc = desc
        self.link = link
        self.date = date # FIXME parse date

    def __repr__(self):
        return '<Event %r>' % self.title

    def serialize(self):
        ret = {}
        ret['lng'] = str(self.lng)
        ret['lat'] = str(self.lat)
        ret['address'] = self.address
        ret['title'] = self.title
        ret['desc'] = self.desc
        ret['date'] = str(self.date)
        ret['link'] = str(self.link)
        ret['owner'] = self.owner.name
        return ret

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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST', 'DELETE'])
def give_data():
    if request.method == 'GET':
        events = Event.query.all()
        items = []
        for event in events:
            items.append(event.serialize())

        payload = {'count': len(items), 'items': items}
        payload = json.dumps(payload)

        resp = Response(payload, status=200, mimetype='application/json')
        return resp

    elif request.method == 'POST':
        data = request.json
        try:
            owner = Owner.query.filter_by(name=data['owner']).first()
            if owner is None:
                owner = Owner(data['owner'])
                db.session.add(owner)
                db.session.commit()

            event = Event(data['address'], data['title'], owner, data.get('desc') , data.get('link'), data.get('date'))
            db.session.add(event)
            db.session.commit()
        except KeyError as e:
            return jsonify({'status': 'KeyError failure', 'error': repr(e)})
        except Exception as e:
            return jsonify({'status': 'Unknown failure', 'error': repr(e)})
        
        return jsonify({'status': 'saved'})

    else:
        pass

    return jsonify({'status': 'nope'})

if __name__ == "__main__":
    app.run(debug=True)
