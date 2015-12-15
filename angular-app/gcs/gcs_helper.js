/**
*  @author: JBayron
*  @source: https://cloud.google.com/storage/docs/json_api/v1/json-api-javascript-samples
*/

$(function(){
  /**
   * Settings
   */

  var Settings = {API_VERSION : 'v1',
                  CLIENT_ID : '',
                  API_KEY : '',
                  BUCKET : '',
                  FULL_SCOPE: 'https://www.googleapis.com/auth/devstorage.full_control',
                  ROLE: '',
                  ENTITY: 'allUsers'
                 };  
  
  /* load and initialize gcs api*/
  function init() {
      gapi.client.load('storage', API_VERSION);
  }

  function list_objects(){
    var request = gapi.client.storage.storage.list(
      {
        'bucket': Settings.BUCKET
      }
    );

    exec(request, 'listObjects');
  }


  function uploadObject(event){
    try{
      var fileData = event.target.files[0];
    }catch(e){
      
    }
    var boundary = '-------314159265358979323846';
    var delimiter = "\r\n--" + boundary + "\r\n";
    var close_delim = "\r\n--" + boundary + "--";

    var reader = new FileReader();
    reader.readAsBinaryString(fileData);
    reader.onload = function(e) {
      var contentType = fileData.type || 'application/octet-stream';
      var metadata = {
        'name': fileData.name,
        'mimeType': contentType
      };

      var base64Data = btoa(reader.result);
      var multipartRequestBody =
          delimiter +
          'Content-Type: application/json\r\n\r\n' +
          JSON.stringify(metadata) +
          delimiter +
          'Content-Type: ' + contentType + '\r\n' +
          'Content-Transfer-Encoding: base64\r\n' +
          '\r\n' +
          base64Data +
          close_delim;

      
      //Use the generic HTTP request method gapi.client.request() to support uploading of large file
      var request = gapi.client.request({
        'path': '/upload/storage/' + Settings.API_VERSION + '/b/' + Settings.BUCKET + '/o',
        'method': 'POST',
        'params': {'uploadType': 'multipart'},
        'headers': {
          'Content-Type': 'multipart/mixed; boundary="' + boundary + '"'
        },
        'body': multipartRequestBody});
      //Remove the current API result entry in the main-content div
      listChildren = document.getElementById('main-content').childNodes;
      if (listChildren.length > 1) {
        listChildren[1].parentNode.removeChild(listChildren[1]);
      }
      try{
        //Execute the insert object request
        exec(request, 'insertObject');
        /*TO DO:
         * make call to the backend to save the object name
         */
        object = fileData.name;         
      }
      catch(e) {
        alert('An error has occurred: ' + e.message);
      }
    }
    
  }

  /*request execution function*/
  function exec(request, request_name){
    /**
       @params:
       request -> is a gapi client storage object
     */
    request.execute(function(resp){
      /*TO DO:
        handle response
      */
    });
  }

  init();
});
