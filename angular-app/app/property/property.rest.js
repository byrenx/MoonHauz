(function(){
  'use srtrict';

   angular
    .module('app.services')
    .service('PropertyREST', PropertyREST);

    PropertyREST.$inject = [
      '$http'
    ];

    function PropertyREST(http){
       var base_url = '/api/property';

       this.list_all = function(){
        return http.get('/api/properties');
       }

    }

})(window.angular);
