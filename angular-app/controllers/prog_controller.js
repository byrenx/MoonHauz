appControllers.controller('ProgressDemoCtrl', function ($scope, BarmService) {
	$scope.max = 0;
	$scope.dynamic = 0;
    $scope.getBank = function()	{
		BarmService.getProjects()
		    .success(function(data,status)	{
				var formax = data.items;
				var myMax = 0;
				console.log(formax.length);
				for (i = 0; i < formax.length; i++)	{
				     myMax += formax[i].billable_hours;
				}
				$scope.max = myMax;
		    })
		    .error(function(data,status)	{
				$scope.max = 0;
		    });

		BarmService.getAllocation()
		    .success(function(data,status)	{
				var fordyn = data.items;
				var myDynamic = 0;
				console.log(fordyn);
				for (d = 0; d < fordyn.length; d++)	{
				     myDynamic += fordyn[d].alloc_hours;
				}
				$scope.dynamic = myDynamic;
		    })
		    .error(function(data,status)	{
		    })

		$scope.type = 'success';

    }
  	$scope.getBank();
});
