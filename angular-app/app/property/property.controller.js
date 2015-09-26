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
    vm.model = Property;
    vm.list = [];
    vm.data = null;

    //functions
    vm.list_all = list_all;
    vm.lands = lands;
    vm.houseAndLots = houseAndLots;
    vm.condoUnits = condoUnits;
    vm.apartments = apartments;

    vm.next = next;
    vm.previous = previous;
    
    function init(){
      vm.list_all();
    }

	  function list_all(){
      Property.list_all();
      vm.model = Property;
    }

    function lands(){
      Property.lands();
      vm.data = Property.data;
    }

    function houseAndLots(){
      Property.houseAndLots();
      vm.data = Property.data;
    }

    function condoUnits(){
      Property.condoUnits();
      vm.data = Property.data;
    }

    function apartments(){
      Property.apartments();
      vm.data = Property.data;
    }

    function next(){
      Property.next();
      //vm.model = Property;
      //console.log(vm.model.next_page);
    }

    function previous(){
      Property.previous();
      //vm.model = Property;
    }

    init();
  }

})(window.angular);
