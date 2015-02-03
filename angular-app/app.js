var AppServices = angular.module('app.services', []);
var AppDirectives = angular.module('app.directives', []);
var AppFilters = angular.module('app.filters', []);
var AppControllers = angular.module('app.controllers', []);
var AppCore = angular.module('app.core',['ngCookies', 'ngRoute', 'ui.bootstrap']);
var AppBarm = angular.module('app.barm', ['ngCookies', 'ngRoute']);

var MainAppModule = angular.module('NgApp', [
    'app.core',
    'app.barm',
    'app.services',
    'app.directives',
    'app.filters',
    'app.controllers'
]);
