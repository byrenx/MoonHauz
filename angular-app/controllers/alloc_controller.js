appControllers.controller('allocateCtrl', function ($scope, $modalInstance, items, BarmService){
    $scope.allocate = {}; //model for project
    $scope.data = {} //return data fron service to be returned
    $scope.projects = {}
    $scope.getProjects = function(){
	BarmService.getProjects()
	    .success(function(data, status){
		$scope.projects = data.items;
		$scope.selected = $scope.projects[0];
	    })
	    .error(function(data, status){
		
	    });	
    };

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
    
    $scope.getProjects();


    //my todo app for testing

    $scope.todos = [];
    $scope.hours = [];
    $scope.addTodo = function () {
      $scope.todos.push($scope.todo);
      $scope.hours.push($scope.hour);
	$scope.todo = '';
	$scope.hour = '';

    };
    
    $scope.removeTodo = function (index) {
      $scope.todos.splice(index, 1);
      $scope.hours.splice(index, 1);
	
    };
    
    
});
