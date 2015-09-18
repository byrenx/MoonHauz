(function(angular){
    "use restrict";

    angular.module('admin.controllers')
     .controller('Properties', properties);

    properties.$inject = [
	    'pubsub',
	    'Property',
    ];

    function properties(pubsub, Property){

      this.modal = modal;
      this.editModal = editModal;
      this.types = Property.types;
      this.land_types = Property.land_types;
      this.list = Property.list;

      this.show_info = show_info;

      activate();

      function activate(){
        Property.list_all();
        GoogleMap.initialize(document.getElementById('map-canvas'), null, {x: 40.7711329, y:-73.9741874});
      }

      function show_info(property_info){
        Property.entity = property_info;
        this.info = property_info;
        GoogleMap.setMarker(this.info.geo_point.lat, this.info.geo_point.lon);
      }

      function modal(){
        Property.entity = {};
        pubsub.publish('modal:propertModal:show');
      }

      function editModal(){
        pubsub.publish('modal:propertModal:show');
      }

    }

})(window.angular);
