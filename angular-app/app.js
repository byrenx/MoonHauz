var appRoutes = angular.module('app.routes', ['ngRoute']);
var appControllers = angular.module('app.controllers', []);
var appServices = angular.module('app.services', []);
var appDirectives = angular.module('app.directives', []);

var mailApp = angular.module("mailApp", ['app.routes',
					 'ui.select',
					 'app.controllers',
					 'app.services',
					 'app.directives',
					 'ui.bootstrap',
					 'ui.utils',
					 'ngAnimate',
					 'ngCookies',
					 'ngResource',
					 'ngSanitize',
					 'ngTouch'
					]
			    );

