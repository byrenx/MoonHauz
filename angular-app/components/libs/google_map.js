/**
*@author Jofel Bayron
*@created Aug. 9, 2015
*/

var GoogleMap = (function(){

  function Map(){

  }

  Map.initialize = initialize;
  Map.map = null;
  Map.default_option = {zoom: 13};

  
  function initialize($canvas, $map_options, $center){
  	var position = new google.maps.LatLng($center.x, $center.y);

    Map.map = new google.maps.Map($canvas, ($map_options !== null? $map_options: Map.default_option));
    Map.map.setCenter(position);
    //set Marker
    Map.setMarker(position);
  }

  function setMarker(position){
    var marker = new google.maps.Marker({position: position, map: Map.map});
  	Map.map.panTo(position);
  }

  return Map;
})();