appControllers.controller('calendarCtrl', function($scope){
    $(document).ready(function() {
	var events_list = [
            {
		title  : 'beckTaxi',
		start  : '2015-02-09'
            },
            {
		title  : 'Chicos',
		start  : '2015-02-09',
		end    : '2015-02-11'
            },
            {
		title  : 'event3',
		start  : '2010-01-09 12:30:00',
		allDay : false // will make the time show
            }
	]
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
		 eventColor: '#378006'

    });


	
});
 


});
