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

      var vm = this;
      vm.types = Property.types;
      vm.land_types = Property.land_types;
      vm.save = save;
      vm.cancel = cancel;
      vm.model = Property;
      vm.setLocationSearch = setLocationSearch;


      function setLocationSearch(elm){
        $('.pac-container').css('z-index', 1052);
        GoogleMap.initPlacesSearchbox(document.getElementById('location'));
      }

      function save(){
        if (Property.entity.key){// update
          Property.update(scope);
        }else{// create
          Property.create(scope);
        }
      }

      function cancel(){
        scope.callback();
        // Property.entity = {};
        // Property.info = {};
        // vm.entity = Property.entity;
      }

    }

})(window.angular);
