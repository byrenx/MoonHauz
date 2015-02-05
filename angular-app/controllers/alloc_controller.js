appControllers.controller('allocateCtrl', function ($scope, $modalInstance, items, BarmService, $sce){
    $scope.allocate = {}; //model for project
    $scope.data = {}; //return data fron service to be returned
    $scope.allocation = {};
    $scope.selected = {};
    $scope.getProjects = function(){
	BarmService.getProjects()
	    .success(function(data, status){
		$scope.projects = data.items;
		$scope.selected['project_id'] = $scope.projects[0];
	    })
	    .error(function(data, status){
		
	    });	
    };

    //my todo app for testing
    $scope.resources = [];
    $scope.hours = [];
    $scope.addTodo = function () {
      $scope.resources.push($scope.resource);
      $scope.hours.push($scope.hour);
	$scope.resource = '';
	$scope.hour = '';

    };
    
    $scope.removeTodo = function (index) {
      $scope.resources.splice(index, 1);
      $scope.hours.splice(index, 1);
    };

    $scope.allocation['alloc_hours'] = $scope.hours;
    $scope.allocation['resource_name'] = $scope.resources;
   
    
    $scope.ok = function(){
	console.log($scope.selected['project_id'].key.urlsafe);    
	$scope.allocation['project_id'] = $scope.selected['project_id'].key.urlsafe;
	BarmService.addAllocation($scope.allocation)
	    .success(function(data, status){
		$scope.data = data.name+", "+data.total_hours;
		$("#form_message").removeClass().addClass("alert alert-success").html("Add project success!");
		$scope.selected = data.name+", "+data.total_hours;
		$modalInstance.close($scope.selected);
		//console.log($scope.data)
	    })
	    .error(function(data, status){
		$("#error_msg").removeClass().addClass("text text-danger").html("Add Project Failed!");
	    });
    }
    $scope.cancel = function () {
	$modalInstance.dismiss('cancel');
    };
    
    $scope.getProjects();



    
    
});
