(function(angular){
    angular.module('app')
	.config(routes);

    routes.$inject = ['$routeProvider', '$locationProvider'];

    function routes(routeProvider, locationProvider){
	routeProvider
	    .when('/admin',{
    		templateUrl : 'ng/templates/admin-index.html'
    		controller  : '',
    		controllerAs: '',
	    })
	    .otherwise(
		    redirectTo: '/admin'
	    )
    }

})(window.angular);
