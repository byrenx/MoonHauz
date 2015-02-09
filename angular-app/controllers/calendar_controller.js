appControllers.controller('calendarCtrl', function($scope, BarmService){
    $scope.events = []
    

    $(document).ready(function() {

	BarmService.getCalendar()
	    .success(function(data,status){
		
		var p = data.items;
		for (i=0; i< p.length; i++){
		    var params = {
			title:p[i].project_name,
			start:''+p[i].alloc_date.year+"-0"+p[i].alloc_date.month+"-0"+p[i].alloc_date.day+'',
			//end  :''+p[i].alloc_date.year+"-0"+p[i].alloc_date.month+"-0"+p[i].alloc_date.day+''
		    }
		    $scope.events.push(
			params
		    );
		}
		//console.log($scope.events);
	    })
	    .error(function(data, status){
		
	    });

	
	var events_list = $scope.events;
	//console.log(events_list);
	 /*var events_list = [
            {
		title  : 'event1',
		start  : '2015-02-09'
            },
            {
		title  : 'event2',
		start  : '2015-02-08',
		end    : '2015-02-08'
            },
            {
		title  : 'event3',
		start  : '2010-01-09T12:30:00',
		allDay : false // will make the time show
            }
	]*/

	console.log(events_list);
	// page is now ready, initialize the calendar...
	$('#calendar').fullCalendar({


	    // put your options and callbacks here
	    header: {
		left: 'prev,next today',
		center: 'title',
		right: 'month,basicWeek,basicDay',
	    },
	    defaultView: 'basicWeek',
	    events: events_list,

	    contentHeight: 'auto'
		 
	});
    });
});
