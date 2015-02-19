// Allow numbers only
appDirectives.directive('numberOnly', function() {
    return {
        link: function(scope, elm, attrs, ctrl){
           elm.keypress(function(event){
               if(event.which != 8 && isNaN(String.fromCharCode(event.which))){
                   event.preventDefault();
               }
           });
        }
    };
});

appDirectives.directive('numbersLimit', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs){
            element.on('paste blur mouseenter', function(e)  {
                var timer;
                var numonly;
                var sanitized;
                function updateField() {
                    window.clearTimeout(timer);
                    timer = window.setTimeout(function(){
                        num = element.val().replace(/\D/g,'');

                        if (num.length > 5) { sanitized = num.substr(num.length - 5 ); element.val(sanitized); }
                        else{ element.val(num); }
                    },100);
                }
                updateField();
            });

           element.keypress(function(event){
               if(element.val().length >= 5 ){
                   event.preventDefault();
               }
           });

        }
    };
});


// simplified and bubble message added. -ray 09/28
function add_validator(elm)    {
    var viewValue = $(elm).val();
    if(viewValue.length <= 0 || viewValue === undefined){
        elm.siblings().addClass('control-label');
        elm.parent().addClass('has-error');

        if(elm.parent().find('.bubble').length < 1)    {
            var bubble = $('<div>This field is required.</div>').addClass('bubble').click(function() { $(this).hide(); });

            // fix position, special case for input type number
            if(elm.attr('type') == 'text' || elm.attr('type') == 'number' || $('textarea') ) {
                bubble.css({'right': -148,'top':-2});
            }

            // if(elm.hasClass('hrs')) {
            //     bubble.css({'right': -170,'top':29});
            // }

            elm.parent().append(bubble);
        }

        // hide bubble on focus of element
        elm.focus(function()  {
            elm.parent().find('.bubble').hide();
        });
        return true;

    }else{
        elm.siblings().addClass('control-label');
        elm.parent().removeClass('has-error');
        elm.parent().find('.bubble').remove();
        return false;
    }
}


appDirectives.directive('mandatory', function() {
    return {
        required: 'ngModel',
        link: function(scope, elm, attrs, ctrl){
            elm.blur(function(){
                add_validator(elm);
            });
        }
    };
});

// Hook to getResource function. getResource does not work if checkboxes are styled on this case.
appDirectives.directive('clickCheckbox', function() {
    return {
        link: function(scope, elm, attrs){
           elm.click(function(event){
                $(elm).find('input').click();
           });
        }
    };
});

