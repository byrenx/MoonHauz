(function(angular){
    "use restrict";

    angular.module('app.services')
     .factory('Property', property);

    property.$inject = [
       'PropertyREST',
       'loading',
       'passive_messenger',
    ];

    function property(PropertyRest, loading, passive_messenger){

      function Property(){
        this._dbSaved = null;
        this.isLoading = loading.new();
        if (data) {
          this.setData(data);
        }
      }

      Property.types = ["Land", "House and Lot", "Condo"];
      Property.land_types = ["INDUSTRIAL", "COMMERCIAL", "AGRICULTURE", "RESIDENTIAL", "RESORT"];
      Property.loading = loading.new();
      Property.entity = {};
      Property.list = [];
      Property.info = {};

      Property.list_all = list_all;

      Property.prototype = {
        destroy: destroy,
        setData: setData,
        isBusy: isBusy,
      };


      /*static function*/
      function list_all(){
        var call = PropertyRest.list_all();
        Property.loading.watch(call)
          .success(function(d){
            Property.list.push.apply(Property.list, d.properties || []);
            console.log(Property.list);
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
