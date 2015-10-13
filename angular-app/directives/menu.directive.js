(function(angular){
  'use strict';

  angular.module('app')
	  .directive('menu', menu);

  menu.$inject = ['$compile'];

  function owl(compile){
	  return {
	    scope: true,
	    restrict: 'A',
	    link : function(scope, elm, attr){
		    compile(elm.contents())(scope);
        console.log($(elm.child));
	    },
	  }
  }
})(window.angular);
