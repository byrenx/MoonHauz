appControllers.controller('ModalDemoCtrl', function ($scope, $modal, $log) {

  $scope.items = ['item1', 'item2', 'item3'];


  $scope.open = function (size) {

    var modalInstance = $modal.open({
      templateUrl: 'myModalContent.html',
      controller: 'ModalInstanceCtrl',
      size: size,
      resolve: {
        items: function () {
          return $scope.items;
        }
      }
    });

      $scope.openproj = function (size){
	  
      }

      

    modalInstance.result.then(function (selectedItem) {
      $scope.selected = selectedItem;
    }, function () {
      $log.info('Modal dismissed at: ' + new Date());
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
            $("#form_message").removeClass().addClass("alert alert-success").html("Message succesfully sent!");
	    $scope.selected['item'] = data.lastname+", "+data.firstname;
	    $modalInstance.close($scope.selected.item);
            console.log($scope.data)
        })
        .error(function(data, status){
            $("#form_message").removeClass().addClass("alert alert-danger").html("Message sending failed!");
        });
    }
  
  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
