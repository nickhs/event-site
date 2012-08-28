window.addEvent('domready', function() {
  var mapc = new Map();
  var item_list = new Items();
  item_list.addEvent('done-loading', function() {
    mapc.render(item_list);
    render_sidebar(item_list.items);
  });
  item_list.load()
});

var Map = new Class({
  initialize: function() {
    this.init_map();
  },

  init_map: function() {
    var mapOptions = {
      center: new google.maps.LatLng(37.774121, -122.423396),
      zoom: 4,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
    };

    this.map = new google.maps.Map($('map_canvas'), mapOptions);
    return this.map;
  },

  render: function(item_list) {
    item_list.items.each(function(item, idx) {
      var marker = new google.maps.Marker({
        position: new google.maps.LatLng(item.lat, item.lng),
        map: this.map,
        title: item.title,
      });
      marker.item = item;
      item.marker = marker;
      google.maps.event.addListener(marker, 'click', this.onMarkerClick);
      console.log(marker)
    }, this);
  },

  onMarkerClick: function(marker) {
    $('event-details').empty()


    var header = new Element('h4', {
      html: "Event Details"
    });

    var name = new Element('div', {
      'class': 'title',
      html: this.item.title,
    });

    var details = new Element('div', {
      'class': 'details',
      html: this.item.desc,
    });

    header.inject($('event-details'))
    name.inject($('event-details'))
    details.inject($('event-details'))
  },
});

var Item = new Class({
  initialize: function(data) {
    Object.each(data, function(value, key) {
      this[key] = value
    }, this);
  }
});

var Items = new Class({
  Implements: Events,

  items: undefined,
  
  initialize: function() {
    this.items = [];
  },
  
  add: function(item) {
    this.items.push(item);
  },
  
  remove: function(to_remove) {
    if (to_remove) {
      items.each(function(item, idx) {
        if (to_remove == item) {
          this.items.slice(idx, idx+1);
          return;
        }
      });
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

  load: function() {
    this.items = [];

    if (!this.req) {
      this.req = new Request.JSON({
        url: 'data',
        onSuccess: this.success.bind(this) 
      })
    }

    this.req.get()
  },
});

function render_sidebar(items) {
  console.log(items)

  $('loading').dispose()

  items.each(function(item, idx) {
    var container = new Element('li');
    var sidebar = new Element('div', {
      'class': 'sidebar',
    });
    var infocontainer = new Element('div', {
      'class': 'info-container',
    });
    var title = new Element('div', {
      'class': 'title',
      html: item.title,
    });
    var info = new Element('div', {
      'class': 'info',
      html: item.address,
    });

    // Assemble li

    sidebar.inject(container);
    infocontainer.inject(container);
    title.inject(infocontainer);
    info.inject(infocontainer);

    container.inject($('events-list'));
  });
};


