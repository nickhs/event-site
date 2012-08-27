window.addEvent('domready', function() {
  var mapc = new Map();
  var item_list = new Items();
  item_list.addEvent('done-loading', function() {
    mapc.render(item_list);
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
      zoom: 12,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
    };

    this.map = new google.maps.Map($('map_canvas'), mapOptions);
    return this.map;
  },

  render: function(item_list) {
    _this = this;
    Array.each(item_list.items, function(item, idx) {
      var marker = new google.maps.Marker({
        position: new google.maps.LatLng(item.lat, item.lng),
        map: _this.map,
        title: item.title,
      });
      marker.item = item;
      google.maps.event.addListener(marker, 'click', _this.onMarkerClick);
    });
  },

  onMarkerClick: function(marker) {
    var infowindow = new google.maps.InfoWindow({
      content: this.item.title,
    });
    infowindow.open(this.map, this);
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
      Array.each(items, function(item, idx) {
        if (to_remove == item) {
          this.items.slice(idx, idx+1);
          return;
        }
      });
    } else {
      return this.items.pop();
    }
  },

  load: function() {
    this.items = [];
    var _this = this;

    var req = new Request.JSON({
      url: 'data',
      onSuccess: function(data) {
        console.log(data);
        Array.each(data.items, function(item, index) {
          var ev = new Item(item);
          _this.add(ev);
        });
        _this.fireEvent('done-loading');
      }
    }).get();
  },
});
