appControllers.controller('projectCtrl', function ($scope, $modalInstance, items, BarmService){
    $scope.project = {}; //model for project
    $scope.data = {} //return data fron service to be returned
    $scope.items = items;
    $scope.selected = $scope.items[0];
    //Configurations for datepicker angular bootstrap


    
    
    $scope.open = function($event) {
	$event.preventDefault();
	$event.stopPropagation();
	
	$scope.opened = true;
    };
    $scope.dateOptions = {
	formatYear: 'yyyy',
	startingDay: 1
    };
    
    $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
    $scope.format = $scope.formats[1];

    $scope.ok = function(){
	
	BarmService.addProject($scope.project)
	    .success(function(data, status){
		$scope.data = data.name+", "+data.total_hours;
		$("#form_message").removeClass().addClass("alert alert-success").html("Add project success!");
		$scope.selected = data.name+", "+data.total_hours;
		$modalInstance.close($scope.selected);
		$modalInstance.dismiss('cancel');
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



