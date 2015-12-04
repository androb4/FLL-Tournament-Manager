var socket;

if (!('WebSocket' in window)) {
  alert('Your browser does not support web sockets');
} else {
  setup();
}

function updateMatch(data) {
  document.getElementById('matchNumber').innerHTML = data.matchIndex+1;

  if(data.matchList[data.matchIndex] != undefined) {
    document.getElementById('tableName1').innerHTML = data.matchList[data.matchIndex].tables[0];
    document.getElementById('tableName2').innerHTML = data.matchList[data.matchIndex].tables[1];
    document.getElementById('team1').innerHTML = data.matchList[data.matchIndex].teams[0];
    document.getElementById('team2').innerHTML = data.matchList[data.matchIndex].teams[1];
  }
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
  socket = new CheesyWebsocket('/display_audience/websocket', {
    matchList: function(event) { updateMatch(event.data); },
    matchTime: function(event) { updateMatchTime(event.data); },
    matchState: function(event) { handleMatchState(event.data); },
    playSound: function(event) { playSound(event.data); }
  });
}
