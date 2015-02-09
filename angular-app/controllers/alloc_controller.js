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
		console.log($scope.selected['project_id']);
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



    //initalizing models
    $scope.resources = [];
    $scope.hours = [];
    $scope.dates = [];
    $scope.disp_dates = [];
    $scope.hour_counter = parseInt(0);
    $scope.addTodo = function () {
	var counter = 0;
	console.log($scope.selected['project_id'].billable_hours);
	var time = parseInt($scope.selected['project_id'].billable_hours);
	counter  = parseInt($scope.hour) + parseInt($scope.hour_counter);
	if($scope.hour == null || $scope.hour == '' || $scope.hour == 0 || $scope.hour > time){
	    $("#hour_err").focus();
	    //setTimeout( $("#hour_err").hide(), 3000);
	}else if($scope.resource == null || $scope.resource == ''){
	    $("#resource_err").focus();
	    //setTimeout( $("#resource_err").hide(), 3000);
	}else if($scope.disp_date == null || $scope.disp_date == ''){
	    $("#dateString").focus();
	}else if(counter > time){
	    $("#error_msg").show().html("Allocated hours for " + $scope.selected['project_id'].name+ " has been exceeded!");
	    $("#hour_err").focus();
	}else{
	    $scope.resources.push($scope.resource);
	    var dateString = $('#dateString').val();
	    var timestamp = Date.parse(dateString).getTime()/1000;
	    $scope.disp_date = dateString;
	    $scope.date = timestamp;
	    $scope.hours.push($scope.hour);
	    $scope.dates.push($scope.date);
	    $scope.disp_dates.push($scope.disp_date);
	    $scope.resource = null;
	    $scope.hour_counter += parseInt($scope.hour);
	    $scope.hour = null;
	    $scope.date = '';
	    console.log(parseInt($scope.selected['project_id'].billable_hours));
	    $scope.disp_date = null;
	    $("#error_msg").hide();
	    console.log($scope.hour_counter);
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
	$scope.allocation['color'] = $scope.selected['project_id'].color;
	$scope.allocation['name'] = $scope.selected['project_id'].name;
	BarmService.addAllocation($scope.allocation)
	    .success(function(data, status){
		$scope.data = data.name+", "+data.total_hours;
		$("#form_message").removeClass().addClass("alert alert-success").html("Add project success!");
		$scope.selected = data.name+", "+data.total_hours;
		$modalInstance.close($scope.selected);
		//console.log($scope.data)
	    })
	    .error(function(data, status){
		$("#error_msg").removeClass().addClass("alert alert-danger").html("Add Project Failed!");
	    });
    }
    $scope.cancel = function () {
	$modalInstance.dismiss('cancel');
    };
    
    $scope.getProjects();



    
    
});
