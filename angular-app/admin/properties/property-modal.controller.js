(function(angular){
    "use restrict";

    angular.module('admin.controllers')
     .controller('PropertyModal', propertyModal);

    propertyModal.$inject = [
	    'pubsub',
	    'Property',
      '$scope',
    ];

    function propertyModal(pubsub, Property, scope){

      this.types = Property.types;
      this.land_types = Property.land_types;
      this.entity = Property.entity;
      this.save = save;
      this.cancel = cancel;
      this.model = Property;
      this.setLocationSearch = setLocationSearch;

      init();

      function init(){
        this.entity = Property.entity;
      }

      function setLocationSearch(elm){
        $('.pac-container').css('z-index', 1052);
        GoogleMap.initPlacesSearchbox(document.getElementById('location'));
      }

      function save(){
        Property.create(scope);
      }

      function cancel(){
        scope.callback();
      }

    }

})(window.angular);
