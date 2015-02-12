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
		    var inputDay = p[i].alloc_date.day;
		    var inputMonth = p[i].alloc_date.month;
		    var inputYear = p[i].alloc_date.year; //to be added: check if last day of the year.
		    var projectName = p[i].project_name;
		    var resourceName = p[i].resource_name;
		    var color = p[i].color;
		    var title = ""+resourceName+" ("+projectName+")";
		    if(SearchString(resourceName,dupNames)){

		    }else{
			 dupNames.push(resourceName);
			 $scope.teams.push({name: resourceName, id: i, isChecked:true, color: color});
		    }
		      var total = p[i].alloc_hours;
		      var divider = 8;
		      var days = Math.ceil(total/divider);
              var myDate = moment({y: inputYear, M : inputMonth, d : inputDay});
		      /* var myDate = new Date();
		      myDate.setFullYear(inputYear);
		      myDate.setMonth(inputMonth);
		      myDate.setDate(inputDay);
		      console.log(myDate);
		      */
		    do{
    			var exDate;
    			var exMonth;
    			var exYear;
			 if(checkifWeekend(myDate) ){

			 }else{
			    exDate = moment(myDate).date();
			    exMonth = moment(myDate).month();
			    exYear = moment(myDate).year();
			    console.log(exYear);
			    pushEvent(exDate,exMonth,exYear,title,color);
			    total -= 8;
			 }
             myDate = moment(myDate).add(1, 'day');

            }while(total > 0);

		}
		$scope.startCalendar();
            })
            .error(function(data, status){
		$scope.startCalendar();
            });
    }

    function february(day,month){
	return ((day == 28 && month ==2) || (day == 29 && month ==2)) ? true : false;
    }


    function checkifWeekendAndPush(day,month,year,title,color)  {
    var myDate = new Date();
    myDate.setFullYear(year);
    myDate.setMonth(month);
    myDate.setDate(day);


    if(myDate.getDay() == 6){
        //pushEvent(day+2,month,year,title+"sat",color); // returns saturday
    }else if(myDate.getDay() == 0){
        //pushEvent(day+2,month,year,title+"sun",color); // returns saturday
    }else{
        pushEvent(day,month,year,title,color); // not weekend
    }
    }
    function checkifWeekend(myDate) {
        var day = moment(myDate).isoWeekday();
        var ret = (day == 6 || day == 7)? true : false;
    	return ret;

    }



    function checkifLastday(day,month,year){
    var threeone = [1,3,5,7,8,10,12];
    var three = [4,6,9,11];
    var leap = [2];

    if (leapYear(year)){

        if(inMonth(month,threeone)){//endates is 31
        return (day==31) ? true: false;
        }else if(inMonth(month,three)){//endates is 30
        return (day==30) ? true: false;
        }else if(inMonth(month,leap)){//leap year endate is 29
        return (day==29) ? true: false;
       }else{
           return false;
       }
    }else{
        if(inMonth(month,threeone)){//endates is 31
        return (day==31) ? true: false;
        }else if(inMonth(month,three)){//endates is 30
        return (day==30) ? true: false;
        }else if(inMonth(month,leap)){
        return (day==28) ? true: false;
       }else{
           return false;
       }
    }
    }

    function inMonth(month,threeone){
    for (var s=0; s<threeone.length;s++){
        if(month == threeone[s]){
        return true;

        }
    }
    return false;

    }

    function leapYear(year){
    return (year % 4 == 0 || year % 100 == 0) ? true : false;
    }



    function pushEvent(day,month,year,title,color){
    $scope.events.push(
        {
        title : title,
        start : ""+year+"-"+month+"-"+day+"",
        color   : ""+color+""
        }
    );
    }


    $scope.refreshCalendar = function(){
/*    $('#calendar').fullCalendar('removeEventSource',$scope.events);
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

        $('#calendar').fullCalendar('addEventSource',$scope.events);
        })
        .error(function(data, status){
        });*/
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
        defaultView: 'month',
        events: $scope.events,
        droppable:true,
        theme: true,
        //weekends: false,
        contentHeight: 'auto'
    });
    console.log($scope.events);

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
         		    var inputDay = p[i].alloc_date.day;
			    var inputMonth = p[i].alloc_date.month;
			    var inputYear = p[i].alloc_date.year; //to be added: check if last day of the year.
			    var projectName = p[i].project_name;
			    var resourceName = p[i].resource_name;
			    var color = p[i].color;
			    var title = ""+resourceName+" ("+projectName+")";
			    if (p[i].alloc_hours <= 8){//check if the allocated hours is less than 8 and push the event
				checkifWeekendAndPush(inputDay,inputMonth, inputYear, title,color);
			    }else{
				var total = p[i].alloc_hours;
				var divider = 8;
				var days = Math.ceil(total/divider);
				var myDate = new Date();
				myDate.setFullYear(inputYear);
				myDate.setMonth(inputMonth);
				myDate.setDate(inputDay);
				console.log(myDate);
				do{
				    var exDate;
				    var exMonth;
				    var exYear
				    if(checkifWeekend(myDate)){

				    }else{
					var exDate = myDate.getDate();
					var exMonth = myDate.getMonth();
				    var exYear = myDate.getFullYear();
					console.log(exYear);
					pushEvent(exDate,exMonth,exYear,title,color);
					days--;
				    }
				    myDate.setDate(myDate.getDate() + 1);

				}while(days != 0);
			    }//end for checking of allocated hours
			}
		    }
		}
		$('#calendar').fullCalendar('addEventSource',$scope.events);
        })
            .error(function(data,status){

            });
    }

});
