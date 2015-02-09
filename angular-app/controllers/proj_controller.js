appControllers.controller('projectCtrl', function ($scope, $modalInstance, items, BarmService){
    $scope.project = {}; //model for project
    $scope.data = {} //return data fron service to be returned
    $scope.items = items;
    $scope.selected = $scope.items[0];
    //Configurations for datepicker angular bootstrap

    function getRandomColor() {
	var letters = '0123456789ABCDEF'.split('');
	var color = '#';
	for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
    }


    $scope.open = function($event) {
	$event.preventDefault();
	$event.stopPropagation();
	
	$scope.opened = true;
    };

    $scope.formats = ['dd-MMMM-yyyy','MM/dd/yyyy', 'dd.MM.yyyy', 'shortDate'];
    $scope.format = $scope.formats[1];

    $scope.ok = function(){
	$scope.project['color'] = getRandomColor();
	if($scope.project['name'] == null || $scope.project['name'] == ''){
	    $("#namer_err").focus();
	    //setTimeout( $("#hour_err").hide(), 3000);
	}else if($scope.project['billable_hours'] == null || $scope.project['billalbe_hours' ]== ''){
	    $("#hour_err").focus();
	    //setTimeout( $("#resource_err").hide(), 3000);
	}else if($scope.project['start_date'] == null || $scope.project['start_date'] == ''){
	    $("#dateString").focus();
	}else{
	var dateString = $('#dateString').val();
	var timestamp = Date.parse(dateString).getTime()/1000;
	$scope.project['start_date'] = timestamp;
	BarmService.addProject($scope.project)
	    .success(function(data, status){
		$scope.data = data.name+", "+data.total_hours;
		$("#form_message").removeClass().addClass("alert alert-success").html("Add project success!");
		$scope.selected = data.name+", "+data.total_hours;
		$modalInstance.dismiss('cancel');
	    })
	    .error(function(data, status){
		$("#error_msg").removeClass().addClass("text text-danger").html("Add Project Failed!");
	    });
	}
    }
    $scope.cancel = function () {
	$modalInstance.dismiss('cancel');
    };
    
    


    
});



