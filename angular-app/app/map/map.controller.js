(function(angular) {
  'use strict';

  angular
    .module('admin.controllers')
    .controller('Branches', branches);

  branches.$inject = [
    'BranchModel',
    'pubsub',
  ];

  function branches(Branch, pubsub) {
     
  }
})(window.angular);
