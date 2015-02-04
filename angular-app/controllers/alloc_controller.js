appControllers.controller('allocateCtrl', function ($scope, $modalInstance, items, BarmService){
    $scope.allocate = {}; //model for project
    $scope.data = {} //return data fron service to be returned
    $scope.getProjects = function(){
	BarmService.getProjects()
	    .success(function(data, status){
		    $scope.items = data.items;
		    console.log($scope.items);
	    })
	    .error(function(data, status){
		
	    });	
    };
    $scope.getProjects();

    $scope.selected = $scope.items;
  

    $scope.ok = function(){
	
	BarmService.addAllocation($scope.project)
	    .success(function(data, status){
		$scope.data = data.name+", "+data.total_hours;
		$("#form_message").removeClass().addClass("alert alert-success").html("Add project success!");
		$scope.selected = data.name+", "+data.total_hours;
		$modalInstance.close($scope.selected);
		console.log($scope.data)
	    })
	    .error(function(data, status){
		$("#error_msg").removeClass().addClass("text text-danger").html("Add Project Failed!");
	    });
    }
    $scope.cancel = function () {
	$modalInstance.dismiss('cancel');
    };
    
    
});
