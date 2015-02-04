appControllers.controller('ui_controller', function($scope){
    $scope.li_navs_stack = ["li_compose", "li_inbox", "li_sentmails"];
    $scope.activateNavBar = function(li_id){
	for(var i=0; i<$scope.li_navs_stack.length; i++){
	    if (li_id == $scope.li_navs_stack[i]){
		$("#"+li_id).removeClass().addClass("active");
	    }else{
		$("#"+$scope.li_navs_stack[i]).removeClass();
	    }
	}
    }
});
