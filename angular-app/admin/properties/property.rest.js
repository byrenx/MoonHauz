(function(){
  'use srtrict';

   angular
    .module('admin.services')
    .service('PropertyREST', propertyREST);

    propertyREST.$inject = [
      '$http'
    ];

    function propertyREST(http){
       var base_url = '/api/property';

       this.list_all = function(){
        return http.get('/api/properties');
       }

       this.create_land = function(params){
         return http.post(base_url + '/land/create', params);
       }

       this.create_house_and_lot = function(params){
         return http.post(base_url + '/house_and_lot/create', params);
       }

       this.create_condo = function(params){
         return http.post(base_url + '/condo_unit/create', params);
       }

       this.create_apartment = function(params){
         return http.post(base_url + '/apartment/create', params);
       }

    }

})(window.angular);
