appControllers.controller('ProgressDemoCtrl', function ($scope, BarmService) {
  $scope.max = 0;
  $scope.length = 0;
  $scope.random = function() {
    var value = Math.floor((Math.random() * 100) + 1);
    var type;
 
    if (value < 25) {
      type = 'success';
    } else if (value < 50) {
      type = 'info';
    } else if (value < 75) {
      type = 'warning';
    } else {
      type = 'danger';
    }
 
    $scope.showWarning = (type === 'danger' || type === 'warning');
 
    $scope.dynamic = value;
    $scope.type = type;
  };

    filterInt = function (value) {
	if(/^(\-|\+)?([0-9]+|Infinity)$/.test(value))
	    return Number(value);
	return NaN;
    }


    $scope.getBank = function(){
	BarmService.getProjects()
	    .success(function(data,status){
		var p = data.items;
		for (i = 0; i < p.length; i++){
		    $scope.max += p[i].billable_hours;
		   // console.log(p[i].billable_hours);
		   // $scope.dynamic += i+1;
		   // alert(i);
		}
	    })
	    .error(function(data,status){
		
	    });
	$scope.dynamic = 300;
	$scope.type = 'success';
    }
  
  $scope.getBank();
 
  $scope.randomStacked = function() {
    $scope.stacked = [];
    var types = ['success', 'info', 'warning', 'danger'];
 
    for (var i = 0, n = Math.floor((Math.random() * 4) + 1); i < n; i++) {
        var index = Math.floor((Math.random() * 4));
        $scope.stacked.push({
          value: Math.floor((Math.random() * 30) + 1),
          type: types[index]
        });
    }
  };
  $scope.randomStacked();
});
