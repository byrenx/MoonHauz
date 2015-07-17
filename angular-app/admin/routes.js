(function(angular){

  "use restrict";

  angular.module('admin')
	.config(routes);

  routes.$inject = ['$routeProvider', '$locationProvider'];

  function routes(routeProvider, locationProvider){
	   routeProvider
	     .when('/admin',{
    		  templateUrl : 'ng/templates/admin-index.html',
    		  controller  : '',
    		  controllerAs: '',
	     })
	     .otherwise({
         redirectTo : '/admin',
       });
  }

})(window.angular);
