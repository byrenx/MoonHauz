(function(angular){

  "use restrict";

  angular.module('admin')
	.config(routes);

  routes.$inject = ['$routeProvider', '$locationProvider'];

  function routes(routeProvider, locationProvider){
	   routeProvider
	     .when('/properties',{
    		  templateUrl : 'ng/templates/admin-manage-properties.html',
    		  controller  : 'Properties',
    		  controllerAs: 'property',
	     })
	     .otherwise({
	        redirectTo : '/properties',
	     });
  }

})(window.angular);
