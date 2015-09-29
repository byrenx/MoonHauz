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
    this.condo_units = function(){
      return http.get('/api/condo_units');
    }
    this.apartments = function(){
      return http.get('/api/apartments');
    }
    this.paginate = function(url){
      return http.get(url);
    }
    this.search_by_location = function(location){
      return http.get(base_url + '/search_by_location/:' + location);
    }
  }
})(window.angular);
