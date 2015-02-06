appControllers.controller('resourceCtrl', function($scope, $http, BarmService){
    $scope.resources = {};
    $scope.getResources = function(){
	BarmService.getAllocation()
	    .success(function(data, status){
		$scope.resources = data.items;
		console.log($scope.resources);
	    })
	    .error(function(data, status){

	    });
    }
    $scope.getResources();
    
});
