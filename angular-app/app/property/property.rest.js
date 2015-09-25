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
    this.lands = function(){
      return http.get('/api/lands');
    }
    this.house_and_lots = function(){
      return http.get('/api/house_and_lots');
    }
    this.condos = function(){
      return http.get('/api/condos');
    }
    this.apartments = function(){
      return http.get('/api/apartments');
    }
  }
})(window.angular);
