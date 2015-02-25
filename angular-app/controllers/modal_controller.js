appControllers.controller('ModalDemoCtrl', function ($scope, $modal, $log, BarmService) {
  $scope.items = {};
    $scope.open = function (size) {

    var modalInstance = $modal.open(  {
        templateUrl: 'ng/templates/modal/addDevModal.html',
        controller: 'ModalInstanceCtrl',
        size: size,
        resolve: {
          items: function () {
            return $scope.items;
          }
        }
    });
    modalInstance.result.then(function (selectedItem) {
        $scope.selected = selectedItem;
      }, function () {
        $log.info('Modal dismissed at: ' + new Date());
      });
  };

  $scope.openproj = function (size) {

      var modalInstance = $modal.open(  {
      	  templateUrl: 'ng/templates/modal/addProjModal.html',
      	  controller: 'projectCtrl',
      	  size: size,
      	  resolve:{
      	      items: function (){
      		        return $scope.items;
      	       }
      	  }
      });

      modalInstance.result.then(function (selectedItem) {
        $scope.getBank();
      }, function () {
    	  $log.info('Modal dismissed at: ' + new Date());
        $scope.getBank();
      });
  };

    $scope.allocate = function (size){
      	var modalInstance = $modal.open({
      	    templateUrl: 'ng/templates/modal/allocateModal.html',
      	    controller: 'allocateCtrl',
      	    size: size,
            backdrop: true,
      	    resolve:{
      	      items: function (){
      		      return $scope.items;
      	      }
      	    }
	 });

  	modalInstance.result.then(function (selectedItem) {
  	    $scope.refreshCalendar();
        $scope.getBank();
  	}, function () {
  	    $log.info('Modal dismissed at: ' + new Date());
  	    $scope.refreshCalendar();
        $scope.getBank();
  	});
    };


});


// Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $modal service used above.

appControllers.controller('ModalInstanceCtrl', function ($scope, $modalInstance, items, BarmService) {
  $scope.person = {}; //model for person
  $scope.items = items;
  $scope.selected = {
    item: $scope.items[0]
  };
  $scope.data = {};
  $scope.ok = function () {

    BarmService.addPerson($scope.person)
        .success(function(data, status){
	    $scope.data = data.lastname+", "+data.firstname;
            $("#form_message").removeClass().addClass("alert alert-success").html("Add developer success!");
	    $scope.selected['item'] = data.lastname+", "+data.firstname;
	    $modalInstance.close($scope.selected.item);
            console.log($scope.data)
        })
        .error(function(data, status){
            $("#form_message").removeClass().addClass("alert alert-danger").html("Add Developer Failed!");
        });
    }
  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
