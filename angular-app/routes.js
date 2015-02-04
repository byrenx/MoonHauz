appRoutes.config(['$routeProvider',
		function($routeProvider){
		    $routeProvider.
			when('/compose', {
			    templateUrl: '/ngtemplate/compose.html'
			}).
			when('/sentmails', {
			    templateUrl: '/ngtemplate/sentmails.html',
			    controller : 'getEmailsController'
			}).
			when('/inbox', {
			    templateUrl: '/ngtemplate/inbox.html',
			}).
			otherwise({
			    redirectTo: '/inbox'
			});
		}]);
