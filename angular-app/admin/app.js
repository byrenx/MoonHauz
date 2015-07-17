(function(angular) {
  'use strict';

  angular
    .module('cs.utilities', [
      'cs.pubsub',
      'cs.passive-messenger',
      'cs.loading',
      'cs.modal',
    ]);

  angular
    .module('app.services', ['cs.utilities']);

  angular
    .module('app.controllers', [
      'app.services',
    ]);

  angular
    .module('app.directives', ['cs.utilities']);

  angular
    .module('app', [
      'app.services',
      'app.directives',
      'app.controllers',
      'ngRoute',
      'ngSanitize',
    ])
    .run(app);

  app.$inject = ['$log', '$timeout', '$rootScope'];

  function app($log, $timeout, $rootScope) {
    $log.info('Angular App Loaded');
    // $timeout(function() { passive_messenger.success('Loaded'); });
    $rootScope.ngLoadingFinished = true;
  }
})(window.angular);
