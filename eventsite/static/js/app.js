window.addEvent('domready', function() {
  var cityBox = $('search-box').getElement('select');
  var cityList = new CitySelect(cityBox);

  cityList.addEvent('update-map', function(pos) {
    mapc.map.setCenter(pos);
    mapc.map.setZoom(12);
  });

  var mapc = new Map();

  mapc.addEvent('update-bounds', function() {
    area_list.load(mapc.city);
  });

  var area_list = new Items($('area-events').getElement('ul'), 'data');

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
    this.init_map();
    this.bounds = null;
    this.city = null;
  },

  init_map: function() {
    var mapOptions = {
      center: new google.maps.LatLng(37.774121, -122.423396),
      zoom: 12,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      panControl: false,
      mapTypeControl: false,
      zoomControl: false
    };

    this.map = new google.maps.Map($('map_canvas'), mapOptions);

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((function(position) {
        var loc = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        if (loc != undefined) {
          this.map.setCenter(loc);
        }
      }).bind(this));
    }

    google.maps.event.addListener(this.map, 'bounds_changed', (function() {
      if (this.bounds === null) {
        this.updateBounds();
      }
      else if (!this.map.getBounds().intersects(this.bounds) && this.map.getZoom() > 11) {
        this.updateBounds();
      }
    }).bind(this));

    return this.map;
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
  },

  findCity: function(loc) {
    geocoder = new google.maps.Geocoder();
    geocoder.geocode({'latLng': loc}, (function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        results.each(function(item, idx) {
          if (item.types[0] == 'administrative_area_level_2') {
            this.city = item.address_components[0].long_name;
            console.log(this.city);
            this.fireEvent('update-bounds');
            return;
          }
        }, this);
      }
    }).bind(this));
  },

  updateBounds: function() {
    console.log('updateBounds ran');
    this.bounds = this.map.getBounds();
    this.findCity(this.map.getCenter());
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
    console.log("load: " + city);
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
      var sidebar = new Element('div', {
        'class': 'sidebar'
      });
      var infocontainer = new Element('div', {
        'class': 'info-container',
        'data-id': item.id
      });
      var title = new Element('div', {
        'class': 'title',
        html: item.title
      });
      var info = new Element('div', {
        'class': 'info',
        html: item.address
      });

      // Assemble li
      sidebar.inject(container);
      infocontainer.inject(container);
      title.inject(infocontainer);
      info.inject(infocontainer);

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

var CitySelect = new Class({
  Implements: Events,

  cities: [],

  initialize: function(element) {
    this.element = element;
    this.chosen = new Chosen(this.element);
    this.load();
    this.element.addEvent('change', (function() {
      console.log("Event called");
      console.log(this.chosen.result_single_selected.get('text'));

      this.cities.each(function(item, idx) {
        if (item.name == this.chosen.result_single_selected.get('text')) {
          console.log("Found!");
          var pos = new google.maps.LatLng(item.lat, item.lng);
          this.fireEvent('update-map', pos);
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
      new Element('option', {
        text: item.name
      }).inject(this.element);

      var hold = {
        id: item.id,
        name: item.name,
        lat: item.lat,
        lng: item.lng
      };

      this.cities.push(hold);
    }, this);

    this.element.fireEvent('liszt:updated');
  }
});



// FIXME move to item class
function render_details(marker) {
  marker.map.panTo(marker.position);
  marker.map.setZoom(14);

  $('event-details').empty();

  var name = new Element('div', {
    'class': 'title',
    html: marker.item.title
  });

  var details = new Element('div', {
    'class': 'details',
    html: marker.item.desc
  });

  name.inject($('event-details'));
  details.inject($('event-details'));
}
