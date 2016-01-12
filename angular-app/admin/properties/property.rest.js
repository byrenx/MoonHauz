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
      };

      this.get = function(key){
        return http.get('/api/property/:' + key);
      };

      this.paginate = function(url){
        return http.get(url);
      };

      this.create_land = function(params){
        return http.post(base_url + '/land/create', params);
      };

      this.create_house_and_lot = function(params){
        return http.post(base_url + '/house_and_lot/create', params);
      };

      this.create_condo = function(params){
         return http.post(base_url + '/condo_unit/create', params);
      };

      this.create_apartment = function(params){
        return http.post(base_url + '/apartment/create', params);
      };

      this.update_land = function(key, params){
        return http.put(base_url + '/land/update/:' + key, params);
      };

      this.update_house_and_lot = function(key, params){
        return http.put(base_url + '/house_and_lot/update/:' + key, params);
      };

      this.update_condo = function(key, params){
        return  http.put(base_url + '/condo_unit/update/:' + key, params);
      }

      this.update_apartment = function(key, params){
        return http.put(base_url + '/apartment/update/:' + key, params);
      }

      this.set_profile_photo = function(key, params){
        return http.put(base_url + '/set_profile_photo/:' + key, params);
      }
    }
})(window.angular);
