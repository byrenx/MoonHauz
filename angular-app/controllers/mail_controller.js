appControllers.controller('mail_controller', function($scope, $http, MailService){
    $scope.mail = {};


    $scope.composeMail = function(){
	MailService.composeMail($scope.mail)
	    .success(function(data, status){
		$("#form_message").removeClass().addClass("alert alert-success").html("Message succesfully sent!");
	    })
	    .error(function(data, status){
		$("#form_message").removeClass().addClass("alert alert-danger").html("Message sending failed!");
	    });
    }



});


appControllers.controller('getEmailsController', function($scope, $http, MailService){
    $scope.emails = [];
    MailService.emails()
	.success(function(data, status){
	    $scope.emails = data.items;
	})
	.error(function(data, status){
	    alert("Error! Fetching emails");
	});
});
