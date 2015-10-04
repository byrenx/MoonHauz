(function(angular){
  "use restrict";

  angular
    .module('app.services')
    .service('DetailRest', detailRest);

  detailRest.$inject = [
    '$http'
  ];

  function detailRest(http){
    var base_url = '/api/property';
    
    this.get = function(key){
      return http.get(base_url + '/:' + key);
    }
  }
})(window.angular);
