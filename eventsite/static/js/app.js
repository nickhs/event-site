window.addEvent('domready', function() {

  var cityBox = $('search-box').getElement('select');
  var cityList = new CitySelect(cityBox);

  cityList.addEvent('update-map', function(pos, city) {
    mapc.map.setCenter(pos);
    mapc.map.setZoom(12);
    mapc.city = city;
    area_list.load(city);
  });

  var mapc = new Map();

  var area_list = new Items($('area-events').getElement('ul'), 'data');
  area_list.load(mapc.city);

  area_list.addEvent('done-loading', function() {
    mapc.render(area_list);
    area_list.render(mapc.city);
  });

  var feat_list = new Items($('hot-events').getElement('ul'), 'featured');
  feat_list.addEvent('done-loading', function() {
    mapc.render(feat_list);
    feat_list.render();
  });
  feat_list.load();

});

var Map = new Class({
  Implements: Events,

  initialize: function() {
    this.city = 'SF Bay Area';
    var mapOptions = {
      center: new google.maps.LatLng(37.774121, -122.423396),
      zoom: 12,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      panControl: false,
      mapTypeControl: false,
      zoomControl: false
    };

    this.map = new google.maps.Map($('map_canvas'), mapOptions);
    this.fireEvent('load');
  },

  render: function(item_list) {
    item_list.items.each(function(item, idx) {
      var marker = new google.maps.Marker({
        position: new google.maps.LatLng(item.lat, item.lng),
        map: this.map,
        title: item.title
      });
      marker.item = item;
      item.marker = marker;
      google.maps.event.addListener(marker, 'click', this.onMarkerClick);
    }, this);
  },

  onMarkerClick: function(marker) {
    render_details(this);
  }
});

var Item = new Class({
  initialize: function(data) {
    Object.each(data, function(value, key) {
      this[key] = value;
    }, this);
  }
});

var Items = new Class({
  Implements: Events,

  items: undefined,
  url: 'data',
  bound_element: undefined,

  initialize: function(bound_element, endpoint) {
    if (endpoint) {
      this.url = endpoint;
    }

    this.bound_element = bound_element;
    this.items = [];
  },

  add: function(item) {
    this.items.push(item);
  },

  remove: function(to_remove) {
    if (to_remove) {
      items.each(function(item, idx) {
        if (to_remove == item) {
          return this.items.slice(idx, idx+1);
        }
      });
			return null;
    } else {
      return this.items.pop();
    }
  },

  success: function(data) {
    data.items.each(function(item, index) {
      this.add(new Item(item));
    }, this);
    this.fireEvent('done-loading');
  },

  load: function(city) {
    this.items = [];

    if (!this.req) {
      this.req = new Request.JSON({
        url: this.url,
        onSuccess: this.success.bind(this)
      });
    }

    if (city) {
      this.req.get('city='+city);
    }

    else {
      this.req.get();
    }
  },

  render: function(city) {
    if (this.items.length === 0) {
      this.bound_element.getElements('li').each(function(item, idx) {
        if (idx === 0 && city) {
          item.set('text', 'Sorry! We don\'t know about any events in '+city+'. Do you? Email us!');
        } else if (idx === 0) {
          item.set('text', 'There are no featured items currently.');
        } else {
          item.dispose();
        }
      });
      return;
    }

    this.bound_element.getElements('li').dispose();

    this.items.each(function(item, idx) {
      var container = new Element('li');

      var infocontainer = Item.getElementFromTemplate(Item.template, {
        'container_class': 'info-container',
        'id': item.id,
        'title_class': 'event-title',
        'title': item.title,
        'info_class': 'event-info',
        'address': item.address,
        'date_class': 'event-dates',
        'start_date': moment(item.start_date).format('dddd, MMMM Do YYYY'),
        'end_date': moment(item.end_date).format('dddd, MMMM Do YYYY')
      });

      // Assemble li
      infocontainer.inject(container);

      container.inject(this.bound_element);

      container.addEvents({
        click: function() {
          render_details(item.marker);
        },

        mouseenter: function() {
          this.addClass('selected');
        },

        mouseleave: function() {
          this.removeClass('selected');
        }
      });
    }, this);
  }
});

/* The Item Template */

Item.extend({
  template: [
    '<div class="{container_class}" data-id="{id}">',
        '<div class="{title_class}">{title}</div>',
        '<div class="{info_class}">{address}</div>',
        '<div class="{date_class}">{start_date} - {end_date}</div>',
    '</div>'
  ],
  details: [
  '<div class="{container_class}">',
      '<div class="{title_class}">{title}</div>',
      '<div class="{desc_class}">{desc}</div>',
      '<ul class="{details_class}">',
          '<li class="{date_class}">{start_date} - {end_date}</li>',
          '<li class="{payment_class}">{payment}</li>',
          '<li class="{address_class}"><a href="http://maps.google.com/?q={address}">{address}</a></li>',
          '<li class="{link_class}"><a href="{link}">Event Website</a></li>',
      '</ul>',
  '</div>'
  ],

  getElementFromTemplate: function(template, model){
    template = (template.join) ? template.join('') : template;
    model = model || {};

    var el = new Element('div', {
      html: template.substitute(model)
    });

    return el.getFirst().dispose();
  }
});

var CitySelect = new Class({
  Implements: Events,

  cities: [],

  initialize: function(element) {
    this.element = element;
    this.chosen = new Chosen(this.element);
    this.load();
    this.element.addEvent('change', (function() {
      this.cities.each(function(item, idx) {
        if (item.name == this.chosen.result_single_selected.get('text')) {
          var pos = new google.maps.LatLng(item.lat, item.lng);
          $('event-details-container').set('style', 'display: none;');
          var city = this.chosen.result_single_selected.get('text');
          this.fireEvent('update-map', [pos, city]);
          return;
        }
      }, this);
    }).bind(this));
  },

  load: function() {
    this.cities = [];

    if (!this.req) {
      this.req = new Request.JSON({
        url: 'city',
        onSuccess: this.success.bind(this)
      });
    }

    this.req.get();
  },

  success: function(data) {
    this.element.getChildren().dispose();
    data.items.each(function(item, idx) {
      var opt = new Element('option', {
        text: item.name
      });

      opt.inject(this.element);

      var hold = {
        id: item.id,
        name: item.name,
        lat: item.lat,
        lng: item.lng,
        option: opt
      };

      this.cities.push(hold);
    }, this);

    this.element.fireEvent('liszt:updated');
  },

  change: function(city) {
    if (this.element === undefined) {
      return;
    }

    this.cities.each(function(item, idx) {
      if (item.name == city) {
        item.option.set('selected', 'true');
        this.element.fireEvent('liszt:updated');
        return;
      }
    }, this);
  }
});


// FIXME move to item class
function render_details(marker) {
  $('event-details-container').style.display = 'inline-block';

  marker.map.panTo(marker.position);
  marker.map.setZoom(14);

  $('event-details').empty();

  var detailscontainer = Item.getElementFromTemplate(Item.details, {
    'container_class': 'details-container',
    'title_class': 'details-title',
    'title': marker.item.title,
    'desc_class': 'details-desc',
    'desc': marker.item.desc,
    'details_class': 'details-details',
    'date_class': 'details-date',
    'start_date': moment(marker.item.start_date).format('dddd, MMMM Do YYYY'),
    'end_date': moment(marker.item.end_date).format('dddd, MMMM Do YYYY'),
    'payment_class': 'details-payment',
    'payment': marker.item.paid,
    'address_class': 'details-address',
    'address': marker.item.address,
    'link_class': 'details-link',
    'link': marker.item.link
  });

  detailscontainer.inject($('event-details'));

  window.scrollTo(0, 0);
}
