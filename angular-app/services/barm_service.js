AppServices.service('BarmService', function($http){
    return {
	addPerson: function(params){
	    return $http.post('/api/persons/add', params);
	},
	addPorject: function(params){
	    return $http.post('/api/projects/add', params)
	    
	}
	
    };
}
