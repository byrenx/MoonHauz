(function(angular){
  "use restrict";

  angular.module('admin.controllers')
	  .controller('Properties', properties);

  properties.$inject = [
	  'pubsub',
	  'Property'
  ];

  function properties(pubsub, Property){

    var vm = this;
	  vm.modal = modal;
	  vm.editModal = editModal;
	  vm.types = Property.types;
	  vm.land_types = Property.land_types;
	  vm.model = Property;
    vm.uploadPhoto = uploadPhoto;

	  vm.show_info = show_info;
    vm.isLoading = Property.loading;
    vm.photo = Property.photo;
    vm.isListEmpty = isListEmpty;
    
    vm.next = next;
    vm.previous = previous;

	  activate();

	  function activate(){
      Property.list_all();
      GoogleMap.initialize(document.getElementById('map-canvas'), null, {x: 40.7711329, y:-73.9741874});
	  }

	  function show_info(property_info){
      Property.getProperty(property_info.key.urlsafe);
      GoogleMap.setMarker(property_info.geo_point.lat, property_info.geo_point.lon);
	  }

	  function modal(){
      Property.entity = {};
      Property.info = {};
      pubsub.publish('modal:propertyModal:show');
	  }

	  function editModal(){
      pubsub.publish('modal:propertyModal:show');
	  }

    function getFile(event){
      //console.log(event.target.files[0]);
    }

    function uploadPhoto(){
      Property.uploadPhoto();
    }

    function next(){
      Property.next();
    }

    function previous(){
      Property.previous();
    }

    function isListEmpty(){
      return vm.model.list.length === 0;
    }

    // function uploadDocs(){
    //   Property.uploadDocs();
    // }

  }

})(window.angular);
