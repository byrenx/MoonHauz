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
      function create(){
        console.log(Property.entity);
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
