(function(angular){
    "use restrict";

    angular.module('admin.controllers')
     .controller('PropertyModal', propertyModal);

    propertyModal.$inject = [
	'pubsub',
	'Property',
    ];

    function propertyModal(pubsub, Property){
      this.types = Property.types;
    }

})(window.angular);
