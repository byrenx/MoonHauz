(function(angular){

  "use restrict";

  angular.module('app')
	.config(routes);

  routes.$inject = ['$routeProvider', '$locationProvider'];

  function routes(routeProvider, locationProvider){
	   routeProvider
	     .when('/home',{
    		  templateUrl : 'ng/templates/guest-home.html',
    		  controller  : '',
    		  controllerAs: '',
	     })
	     .otherwise({
	        redirectTo : '/home',
	     });
  }

})(window.angular);
