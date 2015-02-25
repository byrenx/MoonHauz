appControllers.controller('allocateCtrl', function ($scope, $modalInstance, items, BarmService, $sce, $modal){
    $scope.allocate = {}; //model for project
    $scope.data = {}; //return data fron service to be returned
    $scope.allocation = {};
    $scope.selected = {};
    $scope.params = {};
    $scope.selected_person = {};
    $scope.addPersonToggle = ['list'];
    $scope.rem_hours;
    /*$scope.selected['project_id']['default'] = "---- Please Select a Project ----";*/
    $scope.getProjects = function() {
    	BarmService.getProjects()
    	    .success(function(data, status){
        		$scope.projects = data.items;
        		$scope.selected['project_id'] = '';
                $("#placeholder-project").show().html("Please Select a project");
                $("#placeholder-resource").show().html("Please Add/Select a resource");
    	    })
    	    .error(function(data, status){

    	    });
    };

    $scope.ProjectAllocations = function(key){
        $("#placeholder-project").hide();
        BarmService.findAllocation(key)
            .success(function(data,status){
                $scope.selected['project_id']['allocations'] = data.items;
                $scope.rem_hours = $scope.selected['project_id'].remaining_hours;
                //console.log(data.items);
            })
            .error(function(data,status){
                $scope.rem_hours = $scope.selected['project_id'].remaining_hours;
            });
    }

    $scope.refreshAllocations = function(key){
        $("#placeholder-project").hide();
        BarmService.findAllocation(key)
            .success(function(data,status){
                $scope.selected['project_id']['allocations'] = data.items;
                //console.log(data.items);
            })
            .error(function(data,status){
            });
    }
    $scope.placeholder = function(){
        $("#placeholder-resource").hide();
    }
    $scope.showAddPerson = function()   {

        var toggleAdd = 'add';
        var toggleList = 'list';
        if($scope.addPersonToggle[0] == 'list'){
            $scope.addPersonToggle = [];
            $scope.addPersonToggle.push(toggleAdd);
            $('#resource_err').show();
            $('#user-icon').removeClass().addClass('fa fa-users');
            $('#person_list').hide();
        }else{
            $scope.addPersonToggle = [];
            $scope.addPersonToggle.push(toggleList);
            $('#resource_err').hide();
            $('#user-icon').removeClass().addClass('fa fa-user-plus');
            $('#person_list').show();
        }
    }

    $scope.getResources = function()    {
        BarmService.getAllResources()
            .success(function(data, status){
                $scope.persons = data.items;
                $scope.selected_person = '';

                //console.log($scope.persons);
            })
            .error(function(data,status){
                $scope.addPersonToggle = ['add'];
                $scope.showAddPerson();

            });
    };
    $scope.removeResource = function(key,index, hours)   {
        $scope.selected['project_id']['allocations'].splice(index, 1);
        BarmService.deleteAllocation(key)
            .success(function(status){
                console.log($scope.selected['project_id']['allocations'][index]);
                $scope.rem_hours+= parseInt(hours);
            })
            .error(function(status){

            });
    }

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



    //initializing models
    $scope.resources = [];
    $scope.hours = [];
    $scope.dates = [];
    $scope.colors = [];
    $scope.disp_dates = [];
    $scope.hour_counter = parseInt(0);

    $scope.addTodo = function () {
    	$scope.color = getRandomColor();
    	var counter = 0;
    	//console.log($scope.selected['project_id'].remaining_hours);
    	var time = parseInt($scope.selected['project_id'].remaining_hours);
    	counter  = parseInt($scope.hour) + parseInt($scope.hour_counter);
        	if($scope.hour == null || $scope.hour == '' || $scope.hour == 0) {
        	    $("#hour_err").focus();
            }else if ($scope.hour > time) {
                $("#hour_err").focus();
        	    $("#error_msg").show().html("Allocated hours for " + $scope.selected['project_id'].name+ " has been exceeded!");
        	/*}else if($scope.disp_date == null || $scope.disp_date == '')   {
        	    $("#dateString").focus();*/
        	}else if(counter > time){
        	    $("#error_msg").show().html("Allocated hours for " + $scope.selected['project_id'].name+ " has been exceeded!");
        	    $("#hour_err").focus();
            }else if(isEmpty($scope.selected['project_id'])){
                $("#error_msg").show().html("Please Select a project");
                $('#ui-select-project').focus();
            }else{
                if(($scope.resource != null && $scope.resource != '') && $scope.addPersonToggle[0] == 'add') {
                    $scope.resources.push($scope.resource);
                    $scope.resource = null;
                    pushOthers();
                    $scope.ok();
                }else if($scope.addPersonToggle[0] == 'list'){
                    if(isEmpty($scope.selected_person)){
                         $("#error_msg").show().html("Please Select a resource");
                         $('#person_list').focus();
                    }else{
                        $scope.resources.push($scope.selected_person.name);
                        pushOthers();
                        $scope.ok();
                    }

                }else{
                    $("#resource_err").focus();
                }
            }

    };

    function isEmpty(instance){
         if (instance=='' || instance==null || instance == 0){
            return true;
         }else{
            return false;
         }
    }
    function pushOthers(){
        //var dateString = $('#dateString').val();
        //var timestamp = Date.parse(dateString).getTime()/1000;
        //$scope.disp_date = dateString;
        //$scope.date = timestamp;
        $scope.hours.push($scope.hour);
        //$scope.dates.push($scope.date);
        //$scope.disp_dates.push($scope.disp_date);
        $scope.colors.push($scope.color);
        $scope.color = null;
        $scope.hour_counter += parseInt($scope.hour);
        $scope.rem_hours -= parseInt($scope.hour);
        $scope.hour = null;
        $scope.date = '';
        $scope.disp_date = null;
        $("#error_msg").hide();
    };

    function clearList(){
        $scope.hours = [];
        $scope.resources = [];
        $scope.colors = [];
    }

    $scope.removeTodo = function (index) {
      $scope.rem_hours += parseInt($scope.hours[index]);
      $scope.resources.splice(index, 1);
      $scope.hours.splice(index, 1);
      $scope.dates.splice(index, 1);
      $scope.disp_dates.splice(index, 1);
    };




    $scope.ok = function(){
        $scope.allocation['alloc_hours'] = $scope.hours;
        $scope.allocation['resource_name'] = $scope.resources;
        $scope.allocation['color'] = $scope.colors;
        $('#error_msg').hide();
    	if($scope.allocation['alloc_hours'].length == 0 || $scope.allocation['resource_name'].length == 0)  {

    	    $("#error_msg").show().html("Please Add resource information!");
                $("#resource_err").focus();

    	}else if($scope.selected['project_id'].remaining_hours == 0 || $scope.selected['project_id'].remaining_hours == null)    {
            $("#error_msg").show().html($scope.selected['project_id'].name+": has no remaining hours!");
        }else  {

    	    $scope.allocation['project_id'] = $scope.selected['project_id'].key;
    	    $scope.allocation['name'] = $scope.selected['project_id'].name;
    	    BarmService.addAllocation($scope.allocation)
    		.success(function(data, status)   {
    		    $scope.data = data.name+", "+data.total_hours;
                $("#pool-btn").addClass("btn-disabled").html("<i id='loading' class='glyphicon glyphicon-refresh glyphicon-refresh-animate'></i> Adding...");
                clearList();
                    setTimeout(function()   {
                        $("#pool-btn").removeClass("btn-disabled").html("Saved!");
                    }, 1000);
                    setTimeout(function()   {
                        $("#pool-btn").removeClass("btn-disabled").html("<i id='pool-msg' class='fa fa-level-down fa-lg'></i> Add to Pool");
                        $scope.getResources();
                        $("#placeholder-resource").show().html("Please Add/Select a resource");
                        $scope.refreshAllocations($scope.allocation['project_id'].urlsafe);
                        $scope.showAddPerson();
                    } , 2000);

            })

    		.error(function(data, status){
    		    $("#error_msg").removeClass().addClass("alert alert-danger").html("Add Project Failed!");
    		});
    	}

    }
    $scope.hoursModal = function(key){
            $scope.key = key;
            var modalInstance = $modal.open(  {
            templateUrl: 'ng/templates/modal/eventModal.html',
            controller: 'eventCtrl',
            size: 'lg',
            resolve: {
              items: function () {
                return $scope.key;
              }
            }
        });
        modalInstance.result.then(function (selectedItem) {
            $scope.selected = selectedItem;
          }, function () {
            $scope.refreshAllocations($scope.selected['project_id'].key.urlsafe);
          });

    }

    $scope.cancel = function () {
	   $modalInstance.dismiss('cancel');
    };


$scope.getProjects();
$scope.getResources();

});
