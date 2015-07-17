angular.module('cs.loading', []).
directive('loading', ['$compile', function ($compile) {
  'use strict';
  return {
    restrict: 'EA',
    scope: {
      'instance': '=loading'
    },
    link: function($scope, elem, attrs){
      var $elem = $(elem),
        src = attrs.src || '/img/loading.gif';

      $elem.html(
        '<img src="'+src+'">'
      );
      $elem.addClass('loading');
      $elem.addClass('hidden');

      $scope.$watch('instance.is_loading', function(v){
        if(v){
          $elem.removeClass('hidden');
        } else {
          $elem.addClass('hidden');
        }
      });
    }
  };
}]).
service('loading', function(){
  var complete = function(instance, q){
    return function(){
      instance._futures.splice(instance._futures.indexOf(q), 1);
      check(instance);
    };
  };

  var check = function(instance){
    instance.is_loading = !!instance._futures.length;
  };

  return {'new': function(){
    return {
      is_loading: false,
      _futures: [],
      watch: function($q){
        this._futures.push($q);
        $q.then(complete(this, $q), complete(this, $q));
        check(this);
        return $q;
      }
    };
  }};
});

