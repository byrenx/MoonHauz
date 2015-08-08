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
      this.types = Property.types;
      this.land_types = Property.land_types;
      this.list = Property.list;

      activate();

      function activate(){
      }

      function modal(){
        pubsub.publish('modal:propertModal:show');
      }

      function cancel(){
        pubsub.publish('modal:propertModal:cancel');
      }

    }

})(window.angular);
