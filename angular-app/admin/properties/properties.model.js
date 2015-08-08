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

      Property.create = create;

      Property.prototype = {
        setData: setData,
        destroy: destroy,
        isBusy: isBusy,
      };

      /*static function*/
      function create(scope){
        var type = Property.entity.type;
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
          }).
          error(function(d){

          });
      }

      /*end of static function*/

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
