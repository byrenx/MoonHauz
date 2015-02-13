appControllers.controller('allocateCtrl', function ($scope, $modalInstance, items, BarmService, $sce){
    $scope.allocate = {}; //model for project
    $scope.data = {}; //return data fron service to be returned
    $scope.allocation = {};
    $scope.selected = {};
    $scope.params = {};
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

    function getRandomColor() {
    	var letters = '0123456789ABCDEF'.split('');
    	var color = '#';
    	for (var i = 0; i < 6; i++ ) {
                color += letters[Math.floor(Math.random() * 16)];
    	}
    	return color;
    }

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
    $scope.colors = [];
    $scope.disp_dates = [];
    $scope.hour_counter = parseInt(0);
    $scope.addTodo = function () {
    	$scope.color = getRandomColor();
    	var counter = 0;
    	console.log($scope.selected['project_id'].remaining_hours);
    	var time = parseInt($scope.selected['project_id'].remaining_hours);
    	counter  = parseInt($scope.hour) + parseInt($scope.hour_counter);
        	if($scope.hour == null || $scope.hour == '' || $scope.hour == 0 || $scope.hour > time) {
        	    $("#hour_err").focus();
        	    $("#error_msg").show().html("Allocated hours for " + $scope.selected['project_id'].name+ " has been exceeded!");
        	}else if($scope.resource == null || $scope.resource == '') {
        	    $("#resource_err").focus();
        	}else if($scope.disp_date == null || $scope.disp_date == '')   {
        	    $("#dateString").focus();
        	}else if(counter > time){
        	    $("#error_msg").show().html("Allocated hours for " + $scope.selected['project_id'].name+ " has been exceeded!");
        	    $("#hour_err").focus();
        	}else  {
        	    $scope.resources.push($scope.resource);
        	    var dateString = $('#dateString').val();
        	    var timestamp = Date.parse(dateString).getTime()/1000;
        	    $scope.disp_date = dateString;
        	    $scope.date = timestamp;
        	    $scope.hours.push($scope.hour);
        	    $scope.dates.push($scope.date);
        	    $scope.disp_dates.push($scope.disp_date);
        	    $scope.colors.push($scope.color);
        	    $scope.resource = null;
        	    $scope.color = null;
        	    $scope.hour_counter += parseInt($scope.hour);
        	    $scope.hour = null;
        	    $scope.date = '';
        	    $scope.disp_date = null;
        	    $("#error_msg").hide();
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
    $scope.allocation['color'] = $scope.colors;

    $scope.ok = function(){

    	if($scope.allocation['alloc_hours'].length == 0 || $scope.allocation['resource_name'].length == 0 || $scope.allocation['alloc_date'].length == 0)  {

    	    $("#error_msg").show().html("Please Add resource information!");
                $("#resource_err").focus();

    	}else  {
    	    console.log($scope.selected['project_id'].key);
    	    $scope.allocation['project_id'] = $scope.selected['project_id'].key;
    	    $scope.allocation['name'] = $scope.selected['project_id'].name;


    	    $scope.params['key'] = $scope.allocation['project_id'];
    	    $scope.params['name'] = $scope.selected['project_id'].name;
    	    $scope.params['billable_hours'] = $scope.selected['project_id'].billable_hours;
    	    $scope.params['start_date'] = $scope.selected['project_id'].start_date;
    	    $scope.params['remaining_hours'] = $scope.selected['project_id'].remaining_hours - $scope.allocation['alloc_hours'];

    	    BarmService.updateProject($scope.params);
    	    BarmService.addAllocation($scope.allocation)
    		.success(function(data, status)   {
    		    $scope.data = data.name+", "+data.total_hours;
                $("#ok-btn").addClass("btn-disabled").html("<span id='loading' class='glyphicon glyphicon-refresh glyphicon-refresh-animate'></span> saving...");
                    setTimeout(function()   {
                        $("#ok-btn").removeClass("btn-disabled").html("Saved!");
                    }, 1000);
                    setTimeout(function()   {
                        $modalInstance.dismiss('cancel');
                    } , 2000);
            })
    		.error(function(data, status){
    		    $("#error_msg").removeClass().addClass("alert alert-danger").html("Add Project Failed!");
    		});
    	}

    }

    $scope.cancel = function () {
	$modalInstance.dismiss('cancel');
    };


$scope.getProjects();


});
