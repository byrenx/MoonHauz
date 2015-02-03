/*jshint browser:true, eqnull:true */
/*global angular:true*/

(function(window, angular, $, undefined) {
'use strict';

/*
    Provides passive messages ala GMail.

    To use, include an element like so inside of your <body> tag:

        <div x-passive-messenger></div>

    Then, in your controller/service, use the passive_messenger service:

        passive_messenger.info('Hello!', 'Say Hi Back', say_hi_callback);

    Available methods are info, success, warning, and error.
*/
angular.module('cs.passive-messenger', ['ng', 'cs.pubsub']).
    service('passive_messenger', ['pubsub', function(pubsub){
        var send = function(message, style, action, action_callback){
            pubsub.publish('message:send', message, style, action, action_callback);
        };

        var send_curry = function(style){
            return function(message, action, action_callback){
                return send(message, style, action, action_callback);
            };
        };

        return {
            info: send_curry('info'),
            success: send_curry('success'),
            error: send_curry('error'),
            warning: send_curry('warning'),
        };
    }]).
    directive('passiveMessenger', ['pubsub',function(pubsub) {
        return {
            restrict: 'EA',
            scope: {},
            replace: false,
            template: '<span ng-bind="message">Message goes here.</span>' +
                '<button type="button" class="close">&times;</button>' +
                '<a ng-show="action" ng-click="action_callback()">{{action}}</a>',
            link: function(scope, elem, attrs){
                var $elem = $(elem),
                    timer,
                    mintimer,
                    canhide;
                $elem.addClass('passive-messenger', 'alert');

                var hide = function(){
                    clearTimeout(timer);
                    timer = false;
                    $elem.removeClass('show');
                };

                pubsub.subscribe('message:send', function(message, style, action, action_callback){
                    clearTimeout(timer);
                    timer = setTimeout(hide, 7000);
                    mintimer = setTimeout(function(){ canhide = true; }, 3000);
                    canhide = false;

                    scope.message = message;
                    scope.action = action;
                    scope.action_callback = action_callback;

                    $elem.removeClass('alert-warning alert-success alert-info alert-error');
                    $elem.addClass('alert-' + (style || 'info'));
                    $elem.addClass('show');
                });

                $elem.click(function(e){
                    e.preventDefault();
                    hide();
                });

                $(document).click(function(e){
                    if(timer && canhide){
                        clearTimeout(timer);
                        timer = setTimeout(hide, 1000);
                    }
                });

                $elem.hover(function(e){
                    clearTimeout(timer);
                }, function(e){
                    timer = setTimeout(hide, 4000);
                });
            }
        };
    }]);
})(window, window.angular, jQuery);
