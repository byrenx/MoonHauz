(function(angular){

  "use restrict";

  angular.module('app')
	  .config(routes);

  routes.$inject = ['$routeProvider', '$locationProvider'];

  function routes(routeProvider, locationProvider){
	  routeProvider
	    .when('/home',{
    		templateUrl : 'ng/templates/guest-home.html',
    		controller  : 'Home',
    		controllerAs: 'home',
	    })
	    .when('/properties/:location',{
		    templateUrl : 'ng/templates/app-properties-list.html',
    		controller  : 'Properties',
    		controllerAs: 'properties',
	    })
	    .when('/properties', {
		    templateUrl : 'ng/templates/app-properties-list.html',
    		controller  : 'Properties',
    		controllerAs: 'properties',
	    })
	    .when('/details', {
		    templateUrl : 'ng/templates/app-property-details.html',
    		controller  : 'PropertyDetails',
    		controllerAs: 'propertydetails',
	    })

	    .otherwise({
	      redirectTo : '/home',
	    });
  }

})(window.angular);
