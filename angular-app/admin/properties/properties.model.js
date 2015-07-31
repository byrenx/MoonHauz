(function(angular){
    "use restrict";

    angular.module('admin.services')
     .factory('Property', property);

    property.$inject = [
	
    ];

    function property(){

      function Property(){
	  
      }

      Property.types = ["Land", "House and Lot", "Condo", "Apartment"];
      
      return Property;
    }

})(window.angular);
