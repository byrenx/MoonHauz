(function(angular){
	angular.module('app')
		.config(routes);

		routes.$inject = ['$routeProvider', '$locationProvider'];

		function routes(routeProvider, locationProvider){
			routeProvider
				.when('/',{
					templateUrl : 'ng/templates/app-index.html'
					controller  : '',
					controllerAs: '',
				})
				.when('/admin',{
					templateUrl : 'ng/templates/admin-index.html'
					controller  : '',
					controllerAs: '',
				})
				.otherwise(
						redirectTo: '/index'
				)
		}

})(window.angular);
