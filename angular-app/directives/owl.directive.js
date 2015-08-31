(function(angular){
    'use strict';

    angular.module('app')
	.directive('owl', owl);

    owl.$inject = ['$compile'];

    function owl(compile){
	return {
	    scope: true,
	    restrict: 'A',
	    link : function(scope, elm, attr){
		compile(elm.contents())(scope);
		$(elm).owlCarousel({
                    navigation : true, // Show next and prev buttons
                    slideSpeed : 300,
                    paginationSpeed : 400,
                    pagination: true,
                    autoPlay: true,
                    singleItem: true,
                    responsive: true,
                    rewindNav: true,
		    itemsScaleUp:true,
		});
	    },
	}
    }
})(window.angular);
