appControllers.controller('eventCtrl', function ($scope, $modalInstance, items, BarmService)  {
$scope.key = items;
$scope.params = [];
$scope.counter = 0;
$scope.events = [];
$scope.prev_end;
$scope.remaining_hrs = 0;
$scope.params = {}
$scope.prev_end = null;
$scope.loaded_events = {};

    $scope.init = function(){

        BarmService.findEvent($scope.key)
            .success(function(data,status){
                $scope.items = data;
                $scope.remaining_hrs += data.remaining_hours;
            })
            .error(function(data,status){

            })
    }
    $scope.load_events =function()  {
        BarmService.loadEvent($scope.key)
            .success(function(data,status){
                $scope.loaded_events = data.items;
                var count = data.items.length;
                var load_string = ""+$scope.loaded_events[count-1].end_date.month+"/"+$scope.loaded_events[count-1].end_date.day+"/"+$scope.loaded_events[count-1].end_date.year+"";
                $scope.prev_end = load_string;
            })
            .error(function(data,status){

            })
    }

    $scope.addEvent = function(){
        if(isEmpty($scope.record.start_date)){
            $("#start-date").focus();
            $("#event_err_msg").show().html("Please select a <b> Start date</b>");
        }else if(isEmpty($scope.record.end_date)){
            $("#start-date").focus();
            $("#event_err_msg").show().html("Please select an <b> End date</b>");
        }else if(isEmpty($scope.record.hour)){
             $("#hour-form").focus();
            $("#event_err_msg").show().html("Please enter a valid <b> hour</b>");
        }else if(getPrevDiff() <= 0){
            $("#start-date").focus();
            $("#event_err_msg").show().html("Start date must be greater than the previous end date assigned");
        }else if($scope.record.hour > 8  || $scope.record.hour <= 0)  {
            $("#hour-form").focus();
            $("#event_err_msg").show().html("invalid! <b>hours</b> must be greater than 0 and less than 8");
        }else if(getDateDiff() < 0)  {
            $("#event_err_msg").show().html("invalid! <b>End date</b> must be <b>greater</b> than or equal to <b>Start date</b>");
            $("#start-date").focus();
        }else{
            var start_date = $('#start-date').val();
            var end_date = $('#end-date').val();
            var diff = getDateDiff();
            var total = (diff+ 1) *$scope.record.hour;
            var start_stamp = Date.parse(start_date).getTime()/1000;
            var end_stamp = Date.parse(end_date).getTime()/1000;
            //$scope.disp_date = dateString;
            $("#event_err_msg").hide();
            if(total > $scope.remaining_hrs){
                $("#hour-form").focus();
                $("#event_err_msg").show().html("invalid! This exceeds the remaining hours.");
            }else{
                    $scope.prev_end = $scope.record.end_date;
                    $scope.remaining_hrs -= total;
                    $scope.events.push({'start_disp' : start_date, 'end_disp' : end_date,
                    'frequency' : $scope.record.hour, 'total' : total, 'start_date' : start_stamp, 'end_date' : end_stamp});


                    $scope.record.start_date = '';
                    $scope.record.end_date = '';
                    $scope.record.hour = null;
            }
        }
    }

    $scope.submit = function(){
        $scope.params['remaining_hours'] = $scope.remaining_hrs;
        $scope.params['events'] = $scope.events;
        $scope.params['allocation_id'] = $scope.items.key;
        BarmService.addEvent($scope.params)
            .success(function(data,status){
                $("#submit-btn").addClass("btn-disabled").html("<i id='loading' class='glyphicon glyphicon-refresh glyphicon-refresh-animate'></i> Adding...");

                    setTimeout(function()   {
                        $("#submit-btn").removeClass("btn-disabled").html("Saved!");
                    }, 1000);

                    setTimeout(function()   {
                        $("#submit-btn").removeClass("btn-disabled").html("<i id='pool-msg' class='fa fa-level-down fa-lg'></i> Add to Pool");
                        $modalInstance.dismiss('cancel');
                    } , 2000);

            })
            .error(function(data,status){

            });
    }



    $scope.removeEvent = function (index) {
      $scope.remaining_hrs += $scope.events[index].total;
      $scope.events.splice(index, 1);

    };

    $scope.rmloadedEvent = function(index,key){
        BarmService.deleteEvent(key)
            .success(function(data,status){
                $scope.remaining_hrs += $scope.loaded_events[index].total_hours;
                $scope.loaded_events.splice(index,1);
            })
            .error(function(data,status){

            })
    }

    function getDateDiff(){
            var a = moment($scope.record.end_date);
            var b = moment($scope.record.start_date);
            ret = a.diff(b, 'days')
            return ret
    }

    function getPrevDiff(){
        if($scope.prev_end == null){
            return 1;
        }else{
            var start = moment($scope.prev_end)
            var old = moment($scope.record.start_date);
            var ret = old.diff(start, 'days')
            console.log(ret);
            return ret;
        }

    }


    function isEmpty(instance){
         return (instance=='' || instance==null || instance == 0) ? true : false;
    }


    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

 //Configurations for datepicker angular bootstrap
    $scope.calendar = {
        opened: {},
        dateFormat: 'MM/dd/yyyy',
        dateOptions: {'starting-day':1, 'ending-day':5},
        disabled: function(date,mode) {return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );},
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
$scope.load_events();

});



