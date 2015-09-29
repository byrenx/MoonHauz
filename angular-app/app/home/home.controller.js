(function(angular){
  "use restrict";
  
  angular.module('app.controllers')
    .controller('Home', home);

  home.$inject = [
	  'pubsub',
  ];

  function home(pubsub){

    var vm = this;
    vm.location_input = null;
    vm.submitSearchByLocation = submitSearchByLocation
    
    function submitSearchByLocation(){
      window.location = '#properties/:' + vm.location_input;
    }
  }

})(window.angular);
