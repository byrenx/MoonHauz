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

      function modal(){
        pubsub.publish('modal:propertModal:show');
      }
	
    }

})(window.angular);
