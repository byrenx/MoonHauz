(function(angular){
  "use restrict";
  
  angular.module('app.controllers')
    .controller('Properties', properties);

  properties.$inject = [
	  'pubsub',
	  'Property',
  ];

  function properties(pubsub, Property){

    var vm = this;
    //variables
    vm.list = [];

    //functions
    vm.list_all = list_all;
    vm.lands = lands;
    vm.houseAndLots = houseAndLots;
    vm.condoUnits = condoUnits;
    vm.apartments = apartments;
    
    function init(){
      vm.list_all();
    }

	  function list_all(){
      Property.list_all();
      vm.list = Property.list;
    }

    function lands(){
      Property.lands();
      vm.list = Property.list;
    }

    function houseAndLots(){
      Property.houseAndLots();
      vm.list = Property.list;
    }

    function condoUnits(){
      Property.condoUnits();
      vm.list = Property.list;
    }

    function apartments(){
      Property.apartments();
      vm.list = Property.list;
    }

    init();
  }

})(window.angular);
