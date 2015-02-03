var appRoutes = angular.module('app.routes', ['ngRoute']);
var appControllers = angular.module('app.controllers', []);
var appServices = angular.module('app.services', []);

var barmApp = angular.module("barmApp", 
    ['app.routes', 
     'app.controllers', 
     'app.services']);
