appControllers.controller('calendarCtrl', function($scope, BarmService){
    $scope.items = {}
    $scope.events = [];
    $scope.selected = {};
    $scope.teams = [];

    function SearchString (str,arr) {
        for (var i = arr.length - 1; i >= 0; i--) {
            return (arr[i] == str) ? true : false;
        };
    }
    $scope.setEvents = function()   {
            $scope.events = [];
            $scope.teams = [];

            BarmService.getCalendar()
            .success(function(data,status)  {
                console.log(data);
              $scope.resources = data;
              p = data;
              var dupNames = [];
              for (i=0; i< p.length; i++)   {
                var inputDay = p[i].alloc_date;
        	    var projectName = p[i].project_name;
        	    var resourceName = p[i].resource_name;
        	    var color = p[i].color;
                var alloc_hours = p[i].alloc_hours
                var title = ""+projectName+" ("+alloc_hours+")";
    	       if(SearchString(resourceName,dupNames))    {

    	       }else  {
                    dupNames.push(resourceName);
                    $scope.teams.push({name: resourceName, id: i, isChecked:true, color: color});
                }
                pushEvent(inputDay, title,color);
            }
                $scope.startCalendar();
            })
            .error(function(data, status){
            $scope.startCalendar();
            });
    };


    function pushEvent(inputDay,title,color)    {
        $scope.events.push({title : title,start : ""+inputDay+"",color   : ""+color+""});
    }


    $scope.refreshCalendar = function() {
            $('#calendar').fullCalendar('removeEventSource',$scope.events);
            $scope.events = [];
            $scope.teams = [];
            BarmService.getCalendar()
            .success(function(data,status){
                    $scope.resources = data;
                    p = data;
                    var dupNames = [];
                for (i=0; i< p.length; i++){
                    var inputDay = p[i].alloc_date;
                    var projectName = p[i].project_name;
                    var resourceName = p[i].resource_name;
                    var color = p[i].color;
                    var alloc_hours = p[i].alloc_hours
                    var title = ""+projectName+" ("+alloc_hours+")";
                    if(SearchString(resourceName,dupNames))   {

                    }else   {
                        dupNames.push(resourceName);
                        $scope.teams.push({name: resourceName, id: i, isChecked:true, color:color});
                    }
                        pushEvent(inputDay, title,color);
                }
                    $('#calendar').fullCalendar('addEventSource',$scope.events);
                })
            .error(function(data, status){

            });
    };

    //function to calculate window height
    function get_calendar_height() {
          return $(window).height() - 300;
    }

    $scope.startCalendar = function()   {
        // page is now ready, initialize the calendar...
        $('#calendar').fullCalendar({
            // put your options and callbacks here
            header: {
                left: ' today',
                center: 'prev , title ,next',
                right: 'month,basicWeek,basicDay',
            },
            defaultView: 'month',
            events: $scope.events,
            droppable:true,
            theme: false,
            height: get_calendar_height(),
            //weekends: false,
            contentHeight: get_calendar_height()
        });
        console.log($scope.events);

    };

    $(document).ready(function() {
        $scope.setEvents();
        $(window).resize(function() {
            $('#calendar').fullCalendar('option', 'contentHeight', get_calendar_height());
        });
    });


    $scope.getResource = function(params)   {
        var t = $scope.teams;
        var name_list = [];

        for (i=0; i< t.length; i++){
            if(t[i].isChecked == true){
                name_list.push(t[i].name);
            }else{

            }
        }

        $('#calendar').fullCalendar('removeEventSource',$scope.events);
            $scope.events = [];
            BarmService.getCalendar()
            .success(function(data,status)  {

              p = data;
              for (i=0; i< p.length; i++)   {
                var inputDay = p[i].alloc_date;
                var projectName = p[i].project_name;
                var resourceName = p[i].resource_name;
                var color = p[i].color;
                var alloc_hours = p[i].alloc_hours
                var title = ""+projectName+" ("+alloc_hours+")";
                  for(n=0; n<name_list.length; n++) {
                   if(name_list[n] == resourceName)   {
                        pushEvent(inputDay, title,color);
        		    }//end for checking of allocated hours
        		}
            }
            $('#calendar').fullCalendar('addEventSource',$scope.events);
        })
        .error(function(data,status){

        });
    }

});
