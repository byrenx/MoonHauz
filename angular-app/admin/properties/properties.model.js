(function(angular){
  "use restrict";

  angular.module('admin.services')
    .factory('Property', property);

  property.$inject = [
    'PropertyREST',
    'loading',
    'passive_messenger',
    'Upload',
    '$timeout'
  ];

  function property(PropertyREST, loading, passive_messenger, Upload, timeout){

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
    Property.next_page = undefined; 
    Property.previous_page = undefined; 
    Property.entity = {};
    Property.list = [];
    Property.info = {};
    Property.photo = {};
    
    Property.create = create;
    Property.uploadPhoto = uploadPhoto;
    Property.list_all = list_all;
    Property.getProperty = getProperty;
    Property.update = update;

    Property.previous = previous;
    Property.next = next;

    Property.prototype = {
      destroy: destroy,
      setData: setData,
      isBusy: isBusy,
    };


    /*static function*/
    function list_all(){
      Property.list = [];
      var call = PropertyREST.list_all();
      Property.loading.watch(call)
        .success(function(data){
          Property.previous_page = data.previous_page;
          Property.next_page = data.next_page;
          Property.list.push.apply(Property.list, data.items || []);
        });
    }


    function previous(){
      Property.list = [];
      var call = PropertyREST.paginate(Property.previous_page);
      Property.loading.watch(call)
        .success(function(data){
          Property.previous_page = data.previous_page;
          Property.next_page = data.next_page;
          Property.list.push.apply(Property.list, data.items || []);
        });
    }

    function next(){
      Property.list = [];
      var call = PropertyREST.paginate(Property.next_page);
      Property.loading.watch(call)
        .success(function(data){
          Property.previous_page = data.previous_page;
          Property.next_page = data.next_page;
          Property.list.push.apply(Property.list, data.items || []);
        });
    }

    function getProperty(key){
      Property.entity = {};
      var call = PropertyREST.get(key);
      Property.loading.watch(call)
        .success(function(data){
          angular.extend(Property.entity, data);
          Property.info = data;
        });
    }

    function update(scope){
      var type = Property.entity.type;
      try{
        Property.entity.geo_point = GoogleMap.location_searched.lat()+ ", " +GoogleMap.location_searched.lng();
        Property.entity.location = GoogleMap.location_address;
      }catch(error){
        delete Property.entity.geo_point;
        delete Property.entity.location;
      }
      delete Property.entity.type;
      key = Property.entity.key;
      delete Property.entity.key;
      
      switch(type){
      case 'Land':
        update_land(key, Property.entity, scope);
        break;
      case 'House and Lot':
        update_house_and_lot(key, Property.entity, scope);
        break;
      case 'Condo':
        update_condo(key, Property.entity, scope);
        break;
      case 'Apartment':
        update_apartment(key, Property.entity, scope);
        break;
      }
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
          passive_messenger.info('New Land Property is successfully added!' );
          window.location.reload();
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
          window.location.reload();
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
          window.location.reload();
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
          window.location.reload();
        }).
        error(function(d){

        });
    }

    /**
    Update Properties
    */
    function update_land(key, params, scope){
      var call = PropertyREST.update_land(key, params);
      Property.loading.watch(call)
        .success(function(d){
          Property.entity = d;
          Property.info = d;
          scope.callback();
          passive_messenger.info('Property is successfully updated!');
        });
    }

    function update_house_and_lot(key, params, scope){
      var call = PropertyREST.update_house_and_lot(key, params);
      Property.loading.watch(call)
        .success(function(d){
          Property.entity = d;
          Property.info = d;
          scope.callback();
          passive_messenger.info('Property is successfully updated!');
        });
    }

    function update_condo(key, params, scope){
      var call = PropertyREST.update_condo(key, params);
      Property.loading.watch(call)
        .success(function(d){
          Property.entity = d;
          Property.info = d;
          scope.callback();
          passive_messenger.info('Property is successfully updated!');
        });
    }

    function update_apartment(key, params, scope){
      var call = PropertyREST.update_apartment(key, params);
      Property.loading.watch(call)
        .success(function(d){
          Property.entity = d;
          Property.info = d;
          scope.callback();
          passive_messenger.info('Property is successfully updated!');
        });
    }

    function uploadPhoto(){
      Property.photo.progress = 1;
      Property.photo.file.upload = Upload.upload(
        {
          url: '/api/upload_photo',
          data: {
            file: Property.photo.file,
            property_key: Property.entity.key.urlsafe
          }
        }
      );

      Property.photo.file.upload
        .then(function(resp){
          timeout(function () {
            Property.photo.result = resp.data;
            Property.photo.progress = 0;
          });
        }, function(evt){
          console.log("Event logging");
          Property.photo.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
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
