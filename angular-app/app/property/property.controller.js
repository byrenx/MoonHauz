(function(angular){
  "use restrict";
  
  angular.module('app.controllers')
    .controller('Properties', properties);

  properties.$inject = [
	  'pubsub',
	  'Property',
    '$routeParams'
  ];

  function properties(pubsub, Property, routeParam){

    var vm = this;
    //variables
    vm.model = Property;
    vm.list = [];
    vm.data = null;

    //functions
    vm.list_all = list_all;
    vm.lands = lands;
    vm.houseAndLots = houseAndLots;
    vm.condoUnits = condoUnits;
    vm.apartments = apartments;
    vm.searchByLocation = searchByLocation;
    vm.isListEmpty = isListEmpty;

    vm.next = next;
    vm.previous = previous;
    
    function init(){
      if (routeParam.location){
        vm.searchByLocation(routeParam.location);
      }else{
        vm.list_all();
      }
    }

	  function list_all(){
      Property.list_all();
    }

    function searchByLocation(location){
      Property.searchByLocation(location);
    }

    function lands(){
      Property.lands();
    }

    function houseAndLots(){
      Property.houseAndLots();
    }

    function condoUnits(){
      Property.condoUnits();
    }

    function apartments(){
      Property.apartments();
    }

    function next(){
      Property.next();
    }

    function previous(){
      Property.previous();
    }

    function isListEmpty(){
      return vm.model.list.length == 0;
    }

    init();
  }

})(window.angular);
