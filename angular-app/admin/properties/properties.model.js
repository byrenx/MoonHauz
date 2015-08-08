(function(angular){
    "use restrict";

    angular.module('admin.services')
     .factory('Property', property);

    property.$inject = [
	     'PropertyREST',
       'loading'
    ];

    function property(PropertyREST, loading){

      function Property(){

      }

      Property.types = ["Land", "House and Lot", "Condo", "Apartment"];
      Property.list = [];
      Property.loading = new loading();

      Property.list_all = list_all;

      function list_all(){
        var call = PropertyREST.list_all();
        Property.loading.watch(call)
         .success(function(d){
           Property.list = d;
         })
         .error(function(){

         });
      }

      return Property;
    }

})(window.angular);
