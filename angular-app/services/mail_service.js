appServices.service('MailService', function($http){
    return {
	composeMail: function(params){
	    return $http.post('/api/mails/compose', params);
	},
	emails : function(){
	    return $http.get('/api/mails/sentmails', {});
	}
    };
});
