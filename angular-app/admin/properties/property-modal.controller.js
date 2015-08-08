(function(angular){
    "use restrict";

    angular.module('admin.controllers')
     .controller('PropertyModal', propertyModal);

    propertyModal.$inject = [
	    'pubsub',
	    'Property',
      '$scope'
    ];

    function propertyModal(pubsub, Property, scope){
  
      this.types = Property.types;
      this.land_types = Property.land_types;
      this.entity = Property.entity;
      this.save = save;
      this.cancel = cancel;
      this.model = Property;

      function save(){
        Property.create(scope);
      }

      function cancel(){
        scope.callback();
      }

    }

})(window.angular);
