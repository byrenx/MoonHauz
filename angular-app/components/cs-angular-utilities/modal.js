/*jshint browser:true, eqnull:true */
/*global angular:true*/

(function(window, angular, $, undefined) {
'use strict';

angular.module('cs.modal', ['ng']).
  directive('modal', ['pubsub', function(pubsub){
    return {
      scope: true,
      restrict: 'EA',
      link: function(scope, elm, attrs){
        var $elm = $(elm),
          modal_name = attrs.modal || attrs.id,
          hide_callback;

        pubsub.subscribe('modal:' + modal_name + ':show', function(model, callback, _hide_callback){
          hide_callback = _hide_callback;
          scope.modal.show();

          // Make a copy of the model passed in.
          scope.model = angular.copy(model || {}, {});

          // Setup the callback
          scope.callback = function(){
            if(scope.on_callback) scope.on_callback.apply(this, arguments);

            // Copy our copy of model back to the original.
            angular.copy(scope.model, model);

            pubsub.publish.apply(
              this,
              ['modal:' + modal_name + ':done'].concat(
                Array.prototype.slice.call(arguments)));
            if(callback) callback.apply(this, arguments);
            scope.modal.hide();
          };

          // Call on show to inform the controller that the modal has been shown.
          if(scope.on_show) scope.on_show();

          // Apply, in case this came from outside of angular.
          if (!scope.$$phase) {
            scope.$apply();
          }
        });

        scope.modal = {
          show: function(){
            $elm.modal('show');
          },
          hide: function(){
            if(scope.on_hide) scope.on_hide();
            $elm.modal('hide');
          },
          temporary_hide: function(){
            $elm.modal('hide');
          },
          temporary_show: function(){
            $elm.modal('show');
          },
          name: modal_name
        };

        $elm.on('hidden.bs.modal', function(){
          if(hide_callback) hide_callback();
        });
      }
    };
  }]).
  directive('modalHeader', function(){
    return {
      replace: true,
      transclude: true,
      scope: false,
      template: '<div class="modal-header">' +
        '<button type="button" class="close" ng-click="modal.hide();">&times;</button>'+
        '    <h4 class="modal-title" ng-transclude></h4>'+
        '</div>'
    };
  });

})(window, window.angular, jQuery);
