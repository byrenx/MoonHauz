(function(){
  'use srtrict';

  angular
    .module('app.services')
    .service('PropertyREST', propertyREST);

  propertyREST.$inject = [
    '$http'
  ];

  function propertyREST(http){
    var base_url = '/api/property';

    this.list_all = function(){
      return http.get('/api/properties');
    }

  }

})(window.angular);
