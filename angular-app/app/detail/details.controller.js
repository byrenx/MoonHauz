(function(angular){
    "use restrict";

    angular.module('app.controllers')
     .controller('Details', details);

    details.$inject = [
      'Detail',
      '$routeParams',
    ];

    function details(Detail, routeParams){
      var vm = this;
      vm.detail = Detail.detail;
      vm.getDetail = getDetail;

      vm.model = Detail;

      activate();

      function activate(){
        vm.getDetail();
        GoogleMap.initialize(document.getElementById('map-canvas'), null, {x: 40.7711329, y:-73.9741874});
      }
      
      function getDetail(){
        var key = routeParams.key;
        vm.model = Detail.get(key);
      }

    }
})(window.angular);
