appControllers.controller('ProgressDemoCtrl', function ($scope, BarmService) {
  $scope.length = 0;

    $scope.getBank = function(){
	$scope.max = 0;
	$scope.dynamic = 0;
	BarmService.getProjects()
	    .success(function(data,status){
		var formax = data.items;
		console.log(formax.length);
		for (i = 0; i < formax.length; i++){
		    $scope.max += formax[i].billable_hours;
		    // console.log(p[i].billable_hours);
		    // $scope.dynamic += i+1;
		    // alert(i);
		}
	    })
	    .error(function(data,status){
		$scope.max = 0;
	    });

	BarmService.getAllocation()
	    .success(function(data,status){
		//$scope.dynamic += 
		var fordyn = data.items;
		for (d = 0; d < fordyn.length; d++){
		    $scope.dynamic += fordyn[d].alloc_hours;
		}
		console.log($scope.dynamic);
		
	    })
	    .error(function(data,status){
	    })
    
	$scope.type = 'success';
    }

  
  $scope.getBank();
 

});
