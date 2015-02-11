appControllers.controller('calendarCtrl', function($scope, BarmService){
    $scope.items = {}
    $scope.events = [];
    $scope.selected = {};
    $scope.teams = [];


    function SearchString(str, arr){
	for (var i=0; i < arr.length;i++){
	    if(arr[i] == str){
		return true;
	    }else{
		return false;
	    }
	    
	}
    }


    $scope.setEvents = function(){
	$scope.events = [];
	$scope.teams = [];
	BarmService.getCalendar()
	    .success(function(data,status){
		$scope.resources = data.items;
		p = data.items;
		var dupNames = [];
		for (i=0; i< p.length; i++){
		    if(SearchString(p[i].resource_name,dupNames)){

		    }else{
			dupNames.push(p[i].resource_name);		    
			$scope.teams.push({name: p[i].resource_name, id: i, isChecked:true});			
		    }

		    if (p[i].alloc_hours < 8){//check if the allocated hours is less than 8 and push the event
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
		$scope.startCalendar();
	    });
    }
    $scope.refreshCalendar = function(){
	$('#calendar').fullCalendar('removeEventSource',$scope.events);
	$scope.events = [];
	$scope.teams = [];
	BarmService.getCalendar()
	    .success(function(data,status){
		$scope.resources = data.items;
		p = data.items;
		var dupNames = [];
		for (i=0; i< p.length; i++){
		    if(SearchString(p[i].resource_name,dupNames)){
			
		    }else{
			dupNames.push(p[i].resource_name);		    
			$scope.teams.push({name: p[i].resource_name, id: i, isChecked:true});			
		    }

		    if (p[i].alloc_hours < 8){//check if the allocated hours is less than 8 and push the event
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
		$('#calendar').fullCalendar('addEventSource',$scope.events);
	    })
	    .error(function(data, status){
	    });
    }
    
    $scope.startCalendar = function(){
	// page is now ready, initialize the calendar...
	$('#calendar').fullCalendar({
	    // put your options and callbacks here
	    header: {
		left: ' today',
		center: 'prev , title ,next',
		right: 'month,basicWeek,basicDay',
	    },
	    defaultView: 'basicWeek',
	    events: $scope.events,
	    droppable:true,
	    theme: true,
	    //weekends: false,
	    contentHeight: 'auto'
	});
	//console.log($scope.events);

    }


    $(document).ready(function(){
	$scope.setEvents();
    });

    $scope.getResource = function(params){
	var t = $scope.teams
	var name_list = [];
	for (i=0; i< t.length; i++){
	    if(t[i].isChecked == true){
		name_list.push(t[i].name);
	    }else{
		
	    }
	}
	console.log(name_list);
	$('#calendar').fullCalendar('removeEventSource',$scope.events);
	$scope.events = [];
	BarmService.getCalendar()
	    .success(function(data,status){
		p = data.items;
		for (i=0; i< p.length; i++){
		   for(n=0; n<name_list.length; n++){
		       if(name_list[n] == p[i].resource_name){
			   if(p[i].alloc_hours < 8){
			       $scope.events.push({
				   title : ""+p[i].project_name+" ("+p[i].resource_name+")",
				   start : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+p[i].alloc_date.day+"",
				   end : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+p[i].alloc_date.day+"",
				   color   : ""+p[i].color+""});
			   }else{
			       days = Math.ceil(p[i].alloc_hours / 8);
			       alloc_days = p[i].alloc_date.day + days;
			       if(days > 5){
				   skip_weekend = alloc_days+2;
				   $scope.events.push({
					   title : ""+p[i].project_name+" ("+p[i].resource_name+")",
					   end : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+skip_weekend+"",
					   start : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+p[i].alloc_date.day+"",
					   color   : ""+p[i].color+""});
			       }else{
				   $scope.events.push(
				       {
					   title : ""+p[i].project_name+" ("+p[i].resource_name+")",
					   end : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+alloc_days+"",
					   start : ""+p[i].alloc_date.year+"-"+p[i].alloc_date.month+"-"+p[i].alloc_date.day+"",
					   color   : ""+p[i].color+""
				       }
				   );
			       }//end checking of allocated hours
			   }
		       }
		       }
		}
		console.log($scope.events);
		$('#calendar').fullCalendar('addEventSource',$scope.events);
		
	    })
	    .error(function(data,status){
		
	    });
    }

});
