(function(angular){
    "use restrict";

    angular.module('admin.services')
     .factory('Property', property);

    property.$inject = [
       'PropertyREST',
       'loading',
       'passive_messenger',
    ];

    function property(PropertyREST, loading, passive_messenger){

      function Property(){
        this._dbSaved = null;
        this.isLoading = loading.new();
        if (data) {
          this.setData(data);
        }
      }

      Property.types = ["Land", "House and Lot", "Condo", "Apartment"];
      Property.land_types = ["COMMERCIAL", "AGRICULTURE", "RESIDENTIAL"];
      Property.loading = loading.new();
      Property.entity = {};
      Property.list = [];
      Property.info = {};

      Property.create = create;
      Property.list_all = list_all;

      Property.prototype = {
        setData: setData,
        destroy: destroy,
        isBusy: isBusy,
      };


      /*static function*/
      function list_all(){
        var call = PropertyREST.list_all();
        Property.loading.watch(call)
          .success(function(d){
            console.log(d);
            Property.list.push.apply(Property.list, d.items || []);
          });
      }


      function create(scope){
        var type = Property.entity.type;
        Property.entity['geo_point'] = GoogleMap.location_searched.lat()+ ", " +GoogleMap.location_searched.lng();
        Property.entity['location'] = GoogleMap.location_address;
        delete Property.entity.type;
        switch(type){
          case 'Land':
            create_land(Property.entity, scope);
            break;
          case 'House and Lot':
            create_house_and_lot(Property.entity, scope);
            break;
          case 'Condo':
            create_condo(Property.entity, scope);
            break;
          case 'Apartment':
            create_apartment(Property.entity, scope);
            break;
        }
      }

      function create_land(params, scope){
        var call = PropertyREST.create_land(params);
        Property.loading.watch(call)
          .success(function(d){
            Property.entity = {};
            scope.callback(d);
            passive_messenger.info('New Land Property is successfully added!');
          }).
          error(function(d){

          });
      }

      function create_house_and_lot(params, scope){
        var call = PropertyREST.create_house_and_lot(params);
        Property.loading.watch(call)
          .success(function(d){
            Property.entity = {};
            scope.callback(d);
            passive_messenger.info('New House and Lot Property is successfully added!');
          }).
          error(function(d){

          });
      }

      function create_condo(params, scope){
        var call = PropertyREST.create_condo(params);
        Property.loading.watch(call)
          .success(function(d){
            Property.entity = {};
            scope.callback(d);
            passive_messenger.info('New Condo is successfully added!');
          }).
          error(function(d){

          });
      }

      function create_apartment(params, scope){
        var call = PropertyREST.create_apartment(params);
        Property.loading.watch(call)
          .success(function(d){
            Property.entity = {};
            scope.callback(d);
            passive_messenger.info('New Apartment is successfully added!');
          }).
          error(function(d){

          });
      }

      /*end of static function*/

      /**
        *@desc prototype functions
      */

      function setData(data) {
        angular.extend(this, data);
        this._dbSaved = this.key.urlsafe;
      }

      function destroy() {
        var self = this;
        var call = AssessmentREST.delete(self.key.urlsafe);
        self.isLoading.watch(call);
        return call;
      }

      function isBusy() {
        var self = this;
        return !!self.isLoading._futures.length;
      }

      return Property;
    }

})(window.angular);
