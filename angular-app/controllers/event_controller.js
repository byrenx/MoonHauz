appControllers.controller('eventCtrl', function ($scope, $modalInstance, items, BarmService)  {
$scope.key = items;
$scope.params = [];
$scope.counter = 0;
$scope.events = [];
    $scope.init = function(){

        BarmService.findEvent($scope.key)
            .success(function(data,status){
                $scope.items = data;
            })
            .error(function(data,status){

            })
    }
    $scope.addEvent = function(){

    }

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

 //Configurations for datepicker angular bootstrap
    $scope.calendar = {
        opened: {},
        dateFormat: 'MM/dd/yyyy',
        dateOptions: {},
        open: function($event, which) {
            $event.preventDefault();
            $event.stopPropagation();
            if(which == 'dob'){
                $scope.calendar.opened[which] = true;
                $scope.calendar.opened['win'] = false;
            }else{
                $scope.calendar.opened[which] = true;
                $scope.calendar.opened['dob'] = false;
            }

        }
    };

    $scope.formats = ['dd-MMMM-yyyy','MM/dd/yyyy', 'dd.MM.yyyy', 'shortDate'];
    $scope.format = $scope.formats[1];


$scope.init();

});



