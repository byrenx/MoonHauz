appControllers.controller('taskCtrl', function ($scope, $modalInstance, items, BarmService)  {


    $scope.task = {};
    $scope.loadTasks = function(){
        $scope.items = {};
        $scope.items = items;
        BarmService.getTasks()
            .success(function (data,status){
                var p = data.items;
                for (i=0; i<p.length; i++){
                    if(p[i].resource_name == $scope.items.resourceName && p[i].project_name == $scope.items.projectName && p[i].event == $scope.items.alloc_date){
                        $scope.task['taskContent'] = p[i].taskContent;
                    }
                }
            })
            .error(function(data,status){

            });
    };

    $scope.ok = function(){
        if($scope.task['taskContent'] == '' || $scope.task['taskContent'] == null){
              $("#name_err").focus();
        }else{
            $scope.task['resource_name'] = $scope.items.resourceName;
            $scope.task['project_name'] = $scope.items.projectName;
            $scope.task['event'] = $scope.items.alloc_date;
            BarmService.addTask($scope.task)
                .success(function (data,status){
                        $("#ok-btn").addClass("btn-disabled").html("<span id='loading' class='glyphicon glyphicon-refresh glyphicon-refresh-animate'></span> saving...");
                        setTimeout(function()   {
                            $("#ok-btn").removeClass("btn-disabled").html("Saved!");
                        }, 1000);

                        setTimeout(function()   {
                            $modalInstance.dismiss('cancel');
                        } , 2000);
                })
                .error(function(data,status){

                });

        }



    }

    $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
    };

    $scope.loadTasks();

});



