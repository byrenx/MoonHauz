appServices.service('BarmService', function($http){
    return {
    addPerson: function(params){
        return $http.post('/api/persons/create', params);
    },
    addProject: function(params){
        return $http.post('/api/projects/add', params)

    }

    };
});
