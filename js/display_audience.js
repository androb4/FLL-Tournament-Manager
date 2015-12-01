var socket;

if (!('WebSocket' in window)) {
  alert('Your browser does not support web sockets');
} else {
  setup();
}

function updateMatch(data) {
  console.log(data.match)
  document.getElementById('matchNumber').innerHTML = data.matchIndex+1;
  console.log(data.matchIndex)
}

function updateMatchTime(data) {
  document.getElementById('countdown').innerHTML = data.matchTimeString;
}

function handleMatchState(data) {
  if(data.matchState == 4) {
    document.getElementById("countdown").style.color = "red";
  }
  else {
    document.getElementById("countdown").style.color = "black";
  }
}

function playSound(data) {
  if(data.playSound == 'startMatch') {
    new Audio('/sounds/match_start.wav').play();
  }
  if(data.playSound == 'endMatch') {
    new Audio('/sounds/match_end.wav').play();
  }
}

function setup() {
  var path = '/display_audience/websocket';
  socket = new CheesyWebsocket('/display_audience/websocket', {
    currentMatch: function(event) { updateMatch(event.data); },
    matchTime: function(event) { updateMatchTime(event.data); },
    matchState: function(event) { handleMatchState(event.data); },
    playSound: function(event) { playSound(event.data); }
  });
}
