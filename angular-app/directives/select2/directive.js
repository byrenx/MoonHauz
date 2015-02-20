appDirectives.directive('uiSelect', function() {
    function link($scope, $element, $attrs) {
        $scope.map_list_result = [];
        //$scope.$on('test', function(event, result){
        $scope.$on($scope.select2, function(event, result){
            console.log('catched '+$scope.select2+':', event, result);
            $element.parents('div').css('display', '');
            //$rootScope.$broadcast('test', results);
            //$rootScope.$emit('pickupSelection', {});
            //$scope.map_list_result = result;
            for(var i in result){
               $element.append("<option value='"+result[i].reference+"'>"+result[i].formatted_address+"</option>");
            }
            $element.focus()
        });
    }
    return {
        restrict: 'A',
        scope: {
            'select2': '=',
            'ngModel': '='
        },
        link: link
    };
});
