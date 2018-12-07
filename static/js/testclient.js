var socket;
document.addEventListener("DOMContentLoaded", function(event) { 
  namespace = '/signalling';
  socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
});

function get_msg(){
  socket.emit('get_response',{'data':'This String will be returned'});
  socket.on('response', function(msg) {
            console.log(msg.message);
          });
}

