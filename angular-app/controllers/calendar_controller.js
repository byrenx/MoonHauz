appControllers.controller('calendarCtrl', function($scope, BarmService){
    $scope.items = {}
    $scope.events = [];
    $scope.setEvents = function(){
	BarmService.getCalendar()
	    .success(function(data,status){
		
		p = data.items
		for (i=0; i< p.length; i++){
		    if (p[i].alloc_hours < 8){
			$scope.events.push(
			    {
				title : ""+p[i].project_name+" ("+p[i].resource_name+")",
				start : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+p[i].alloc_date.day+"",
				end : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+p[i].alloc_date.day+"",
				color   : ""+p[i].color+""
			    }

			);
		    }else{
			days = Math.ceil(p[i].alloc_hours / 8);
			alloc_days = p[i].alloc_date.day + days;
			if(days > 5){
			    skip_weekend = alloc_days+2;
			    $scope.events.push(
				{
				    title : ""+p[i].project_name+" ("+p[i].resource_name+")",
				    end : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+skip_weekend+"",
				    start : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+p[i].alloc_date.day+"",
				    color   : ""+p[i].color+""
				}
			    );
			}else{
			    $scope.events.push(
				{
				    title : ""+p[i].project_name+" ("+p[i].resource_name+")",
				    end : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+alloc_days+"",
				    start : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+p[i].alloc_date.day+"",
				    color   : ""+p[i].color+""
				}
			    );
			}
		    }
		}
		$scope.startCalendar();
	    })
	    .error(function(data, status){
		
	    });
    }

    
    $scope.startCalendar = function(){
	// page is now ready, initialize the calendar...
	$('#calendar').fullCalendar({
	    // put your options and callbacks here
	    header: {
		left: 'prev,next today',
		center: 'title',
		right: 'month,basicWeek,basicDay',
	    },
	    defaultView: 'basicWeek',
	    events: $scope.events,
	    //weekends: false,
	    contentHeight: 'auto'
	});
	console.log($scope.events);
    }
    $scope.setEvents();



});
