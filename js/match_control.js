$(function() {
  if (!('WebSocket' in window)) {
    alert('Your browser does not support web sockets');
    throw new Error("Something went badly wrong!");
  }

  var path = '/match_control/websocket';
  var url = 'ws://' + window.location.hostname;
  if (window.location.port != "") {
    url += ":" + window.location.port;
  }
  url += path;
  var socket = new WebSocket(url);

  //console.log('socket status: ' + socket.readyState);

  $('#startMatchBtn').click(function() {
    socket.send("start");
  });

  // event handlers for websocket
  if (socket) {

    socket.onopen = function() {}

    socket.onmessage = function(msg) {
      showServerResponse(msg.data);
    }

    socket.onclose = function() {
      showServerResponse('The connection has been closed.');
    }

  } else {
    console.log('invalid socket');
  }

  function showServerResponse(txt) {
    console.log(txt);
  }
});
