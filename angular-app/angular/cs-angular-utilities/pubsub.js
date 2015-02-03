/*jshint browser:true, eqnull:true */
/*global angular:true*/

(function(window, angular, $, undefined) {
'use strict';
/*
    More or less blatantly taken from https://github.com/phiggins42/bloody-jquery-plugins/blob/master/pubsub.js
*/
angular.module('cs.pubsub', ['ng']).
    factory('pubsub', [function() {
        // the topic/subscription hash
        var cache = {};

        return {
            publish: function(topic){
                // example:
                //      Publish stuff on '/some/topic'. Anything subscribed will be called
                //      with a function signature like: function(a,b,c){ ... }
                //
                //  |       $.publish("/some/topic", "a", "b","c");
                var args = Array.prototype.slice.call(arguments, 1);
                return cache[topic] && $.each(cache[topic], function(){
                    this.apply($, args);
                });
            },
            subscribe: function(topic, callback){
                if(!cache[topic]){
                    cache[topic] = [];
                }
                cache[topic].push(callback);
                return [topic, callback]; // Array
            },
            unsubscribe: function(handle){
                // summary:
                //      Disconnect a subscribed function for a topic.
                // handle: Array
                //      The return value from a $.subscribe call.
                // example:
                //  |   var handle = $.subscribe("/something", function(){});
                //  |   $.unsubscribe(handle);

                var t = handle[0];
                return cache[t] && $.each(cache[t], function(idx){
                    if(this == handle[1]){
                        cache[t].splice(idx, 1);
                    }
                });
            }
        };

    }]).
    directive('pubsubEvent', ['$compile', 'pubsub', function ($compile, pubsub){
      return {
        restrict: 'A',
        scope: false,
        link: function ($scope, elm, attrs) {
          var $elm = $(elm);
          var topic = attrs.pubsubEvent;
          var data = attrs.pubsubEventData;
          var stop_prop = attrs.pubsubEventStopPropagation !== undefined;

          $elm.click(function(e){
            e.preventDefault();
            if(stop_prop) e.stopPropagation();
            $scope.$apply(function(){
                pubsub.publish(topic, data);
            });
          });

          /* Prevent Focus Stealing */
          if(stop_prop){
            var stop_func = function(e){e.preventDefault(); e.stopPropagation();};
            $elm.on('mousedown', stop_func);
            $elm.on('mouseup', stop_func);
          }
        }
      };
    }]);
})(window, window.angular, jQuery);
