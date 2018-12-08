$(document).ready(function(){
  namespace = '/signalling';
  socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
  socket.on('sdp_message', function(msg){
    console.log(msg.sdp_message);
  });

  $('form#register_as_user').submit(function(event) {
    socket.emit('register_endpoint_server', {id: $('#register_as_user_data').val(), type:'endpoint'});
    return false;
  });

  $('form#contact_endpoint_server').submit(function(event) {
    socket.emit('contact_endpoint_server', {endpoint_server_id: $('#endpoint_server_id_data').val(), sdp_message:$('#sdp_data').val()});
    return false;
  });
});

