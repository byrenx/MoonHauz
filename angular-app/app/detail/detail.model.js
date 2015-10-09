(function(angular){
  "use restrict";

  angular.module('app.services')
  .factory('Detail', detail);

  detail.$inject = [
    'DetailRest',
    'loading',
    'passive_messenger',
  ];

  function detail(DetailRest, loading, passive_messenger){

    function Detail(){
      this._dbSaved = null;
      this.isLoading = loading.new();
      // if (data) {
      //   this.setData(data);
      // }

    }


    Detail.detail = {};
    Detail.loading = loading.new();

    Detail.get = get;

    
    Detail.prototype =  {
      setData: setData,
    };

    function get(key){
      var detail = new Detail();
      var call = DetailRest.get(key);
      detail.isLoading.watch(call)
        .success(function(data){
          detail.setData(data);
          console.log(data);
          GoogleMap.initialize(document.getElementById('map-canvas'),
                               null,
                               {x: data.geo_point.lat,
                                y: data.geo_point.lon});
        });
      return detail;
    }


    function setData(data) {
      angular.extend(this, data);
      this._dbSaved = this.key.urlsafe;
    }

    return Detail;
  }
  
})(window.angular);
