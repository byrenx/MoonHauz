var moonhauz = (function(){

  function MoonHauz(){}

  MoonHauz.parallax = parallax;
  MoonHauz.jumboHeight = $('#jumbotron').outerHeight();


  function parallax(){
    console.log("Hello World");
    var scrolled = $(window).scrollTop();
    //$('.bg').css('height', (MoonHauz.jumboHeight-scrolled) + 'px');
  }

  return MoonHauz;
})();


$(window).scroll(function(e){
    moonhauz.parallax();
});
