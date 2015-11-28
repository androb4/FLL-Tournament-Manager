function updateMatchList(matches) {
  var table = document.getElementById("matchListTable");

  while (table.rows.length-1 > 0) {
    table.deleteRow(1);
  }

  for (m=0; m<matches.length; m++) {
    var row = table.insertRow(m+1);
    var cell;

    if(m==0)
      row.classList.add("success");

    cell = row.insertCell(0);
    cell.innerHTML = matches[m].matchNumber;

    cell = row.insertCell(1);
    cell.innerHTML = matches[m].matchTime;
  }
}

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

    socket.onopen = function() {

    }

    socket.onmessage = function(msg) {
      document.getElementById('countdown').innerHTML = JSON.parse(msg.data).timeString;
      if (JSON.parse(msg.data).timerStart == 'true')
        $('#startMatchBtn').prop('disabled', true);
      else
        $('#startMatchBtn').prop('disabled', false);
      updateMatchList(JSON.parse(msg.data).matchList)
      showServerResponse(JSON.parse(msg.data))
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
