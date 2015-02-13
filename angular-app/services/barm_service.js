appServices.service('BarmService', function($http){
    return {
    addPerson: function(params){
        return $http.post('/api/persons/create', params);
    },
    addProject: function(params){
        return $http.post('/api/projects/create', params);
    },
    getProjects: function(){
	return $http.get('/api/projects/list', {});
    },
    updateProject: function(params){
	return $http.post('/api/projects/:'+params.key.urlsafe, params);
    },
    addAllocation: function(params){
	return $http.post('/api/allocations/create', params);
    },
    getAllocation: function(){
	return $http.get('/api/allocations/list');
    },
    getCalendar: function(){
	return $http.get('/api/allocations/calendar');
    },

    };
});
