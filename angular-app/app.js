var appRoutes = angular.module('app.routes', ['ngRoute']);
var appControllers = angular.module('app.controllers', []);
var appServices = angular.module('app.services', []);


var mailApp = angular.module("mailApp", ['app.routes', 
					 'app.controllers', 
					 'app.services', 
					 'ui.bootstrap',
					 'ngAnimate',
					 'ngCookies',
					 'ngResource',
					 'ngSanitize',
					 'ngTouch'
					]
			    );
