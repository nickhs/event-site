from flask import render_template, jsonify, request, Blueprint
from models import City, Event, Owner, add_item, delete_item
import config
import datetime

data_api = Blueprint('data_api', 'eventsite')


@data_api.route('/')
def index():
    return render_template('index.html')


@data_api.route('/data', methods=['GET', 'POST', 'DELETE'])
def handle_data():
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
        now = datetime.datetime.now()

        if city is None:
            items = []
        else:
            items = Event.query.filter(Event.city == city, Event.start_date > now).order_by(Event.start_date).limit(10).all()
            items = [convert_to_dict(x) for x in items]
    else:
        items = [convert_to_dict(x) for x in Event.query.limit(5).all()]

    return {'count': len(items), 'items': items}


def handle_post(request):
    data = request.json

    if not data:
        return {'status': 'JSON only buddy'}

    if not data.get('auth', None) == config.AUTH_KEY:
        return {'status': 'unauthorized'}

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

        if error is not None:
            return {'status': 'IntegrityError', 'error': error}

    except KeyError as e:
        return {'status': 'KeyError failure', 'error': repr(e)}
    except Exception as e:
        return {'status': 'Unknown failure', 'error': repr(e)}

    return {'status': 'saved', 'event': convert_to_dict(event)}


def handle_delete(request):
    data = request.json
    event = None

    if not data.get('auth', None) == config.AUTH_KEY:
        return {'status': 'unauthorized'}

    if 'id' in data:
        event = Event.query.get(data['id'])

    elif 'title' in data:
        event = Event.query.filter_by(title=data['title']).first()

    else:
        return {'status': 'failed', 'error': "No valid search specified. Valid search fields are id or name"}

    if event is None:
        return {'status': 'failed', 'error': 'No event found'}

    delete_item(event)
    return {'status': 'success', 'event': convert_to_dict(event)}


@data_api.route('/featured', methods=['GET'])
def give_featured_data():
        events = Event.query.filter_by(featured=True).all()
        items = [convert_to_dict(x) for x in events]
        payload = {'count': len(items), 'items': items}
        return jsonify(payload)


@data_api.route('/owner', methods=['GET'])
def give_owners():
    items = [convert_to_dict(x) for x in Owner.query.all()]
    payload = {'count': len(items), 'items': items}
    return jsonify(payload)


# TODO cache this function
@data_api.route('/city', methods=['GET'])
def give_cities():
    items = [convert_to_dict(x) for x in City.query.all()]
    payload = {'count': len(items), 'items': items}
    return jsonify(payload)


def convert_to_dict(obj):
    ret = {}
    for key, val in obj.__dict__.items():
        if key.startswith('_'):
            continue
        # Broken if unicode
        ret[key] = str(val)

    return ret
