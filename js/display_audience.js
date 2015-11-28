if (!('WebSocket' in window)) {
    alert('Your browser does not support web sockets');
} else {
    setup();
}

function setup() {

    // Note: You have to change the host var
    // if your client runs on a different machine than the websocket server

    var path = '/display_audience/websocket';
    var url = 'ws://' + window.location.hostname;
    if (window.location.port != "") {
        url += ":" + window.location.port;
    }
    url += path;
    var socket = new WebSocket(url);

    //console.log('socket status: ' + socket.readyState);

    // event handlers for websocket
    if (socket) {

        socket.onopen = function() {
            //alert('connection opened....');
        }

        socket.onmessage = function(msg) {
          showServerResponse(msg.data);
          document.getElementById('countdown').innerHTML = JSON.parse(msg.data).timeString;
        }

        socket.onclose = function() {
            //alert('connection closed....');
            showServerResponse('The connection has been closed.');
        }

    } else {
        console.log('invalid socket');
    }

    function showServerResponse(txt) {
      console.log(txt);
    }
}
