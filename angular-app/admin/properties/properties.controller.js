(function(angular){
    "use restrict";

    angular.module('admin.controllers')
     .controller('Properties', properties);

    properties.$inject = [
	'pubsub',
    ];

    function properties(pubsub){
	
      this.modal = modal;

      function modal(){
        pubsub.publish('modal:propertModal:show');
        console.log('modal is triggered');
      }
	
    }

})(window.angular);
