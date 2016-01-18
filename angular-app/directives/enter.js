(function(angular){
  'use strict';

  angular.module('admin')
    .directive('enter', Enter);

  Enter.$inject = ['$compile'];

  function Enter(){
    return {
      scope: true,
      link: function(scope, element, attrs){
        element.bind('keydown keypress', function(event){
          if(event.which === 13){ // enter
            scope.$apply(function(){
              scope.$eval(attrs.enter);
            });

            event.preventDefault();
          }
        });
      }
    };
  }
})(window.angular);
