/**
*@author Jofel Bayron
*@created Aug. 9, 2015
*/

var GoogleMap = (function(){

  function Map(){

  }

  Map.map = null;
  Map.default_option = {zoom: 13};
  Map.search_box = null;

  Map.initialize = initialize;
  Map.setMarker = setMarker;
  Map.initPlacesSearchbox = initPlacesSearchbox;
  Map.location_searched = null;
  Map.location_address = '';
  Map.marker = null;
  
  
  function initialize($canvas, $map_options, $center){
  	var position = new google.maps.LatLng($center.x, $center.y);
    Map.map = new google.maps.Map($canvas, ($map_options !== null? $map_options: Map.default_option));
    Map.map.setCenter(position);
    //set Marker
    Map.setMarker($center.x, $center.y);
  }

  function setMarker(x, y){
  	var position = new google.maps.LatLng(x, y);
    Map.marker = new google.maps.Marker({position: position, map: Map.map});
  	Map.map.panTo(position);
  }

  function initPlacesSearchbox(search_input){
  	Map.search_box = new google.maps.places.Autocomplete(search_input);
  	google.maps.event.addListener(Map.search_box, 'place_changed', function() {
		var place = Map.search_box.getPlace();
		Map.location_searched = place.geometry.location;
		Map.location_address = place.formatted_address;
    });
  }

  return Map;
})();