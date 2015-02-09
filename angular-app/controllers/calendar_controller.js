appControllers.controller('calendarCtrl', function($scope, BarmService){
    $scope.events = []
    

    $(document).ready(function() {

	BarmService.getCalendar()
	    .success(function(data,status){
		var p = data.items;
		for (i=0; i< p.length; i++){
		    $scope.events.push(
			{
			    title  : p[i].project_name,
			    start  : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+p[i].alloc_date.day+"",
			    end    : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+p[i].alloc_date.day+""
			}
		    );
		}
		//console.log($scope.events);
	    })
	    .error(function(data, status){
		
	    });

	

	//console.log(events_list);
	var events_list = [
            {
		title  : 'event1',
		start  : '2015-02-09'
            },
            {
		title  : 'event2',
		start  : '2015-09-02',
		end    : '2015-09-02'
            },
            {
		title  : 'event3',
		start  : '2010-01-09T12:30:00',
		allDay : false // will make the time show
            }
	]
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
