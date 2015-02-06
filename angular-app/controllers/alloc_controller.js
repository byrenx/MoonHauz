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
    //Configurations for datepicker angular bootstrap
    
    $scope.open = function($event) {
	$event.preventDefault();
	$event.stopPropagation();
	
	$scope.opened = true;
    };
    
    $scope.formats = ['dd-MMMM-yyyy','MM/dd/yyyy', 'dd.MM.yyyy', 'shortDate'];
    $scope.format = $scope.formats[1];



    //my todo app for testing
    $scope.resources = [];
    $scope.hours = [];
    $scope.dates = [];
    $scope.disp_dates = [];
    $scope.addTodo = function () {
	if($scope.hour == null || $scope.hour == ''){
	    $("#hour_err").focus();
	    //setTimeout( $("#hour_err").hide(), 3000);
	}else if($scope.resource == null || $scope.resource == ''){
	    $("#resource_err").focus();
	    //setTimeout( $("#resource_err").hide(), 3000);
	}else if($scope.disp_date == null || $scope.disp_date == ''){
	    $("#dateString").focus();
	}else{
	    $scope.resources.push($scope.resource);
	    var dateString = $('#dateString').val();
	    var timestamp = Date.parse(dateString).getTime()/1000;
	    $scope.date = timestamp;
	    $scope.hours.push($scope.hour);
	    $scope.dates.push($scope.date);
	    $scope.disp_dates.push($scope.disp_date);
	    $scope.resource = null;
	    $scope.hour = null;
	    $scope.date = '';
	    $scope.disp_date = null;
	}
    };
    
    $scope.removeTodo = function (index) {
      $scope.resources.splice(index, 1);
      $scope.hours.splice(index, 1);
      $scope.dates.splice(index, 1);
      $scope.disp_dates.splice(index, 1);
    };

    $scope.allocation['alloc_hours'] = $scope.hours;
    $scope.allocation['resource_name'] = $scope.resources;
    $scope.allocation['alloc_date'] = $scope.dates;
    
    $scope.ok = function(){
	console.log($scope.selected['project_id'].key);    
	$scope.allocation['project_id'] = $scope.selected['project_id'].key;
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
