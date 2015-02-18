appControllers.controller('taskCtrl', function ($scope, $modalInstance, items, BarmService)  {

    $scope.task = items;
    console.log($scope.task);

    $scope.ok = function(){

        $("#ok-btn").addClass("btn-disabled").html("<span id='loading' class='glyphicon glyphicon-refresh glyphicon-refresh-animate'></span> saving...");
        setTimeout(function()   {
            $("#ok-btn").removeClass("btn-disabled").html("Saved!");
        }, 1000);

        setTimeout(function()   {
            $modalInstance.dismiss('cancel');
        } , 2000);
    }

    $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
    };

});



