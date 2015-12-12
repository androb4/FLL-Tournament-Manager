var socket;

if (!('WebSocket' in window)) {
  alert('Your browser does not support web sockets');
} else {
  setup();
}

function updateMatch(data) {
  document.getElementById('matchNumber').innerHTML = data.matchIndex+1;

  if(data.matchList[data.matchIndex] != undefined) {
    document.getElementById('tableName1').innerHTML = data.matchList[data.matchIndex][2];
    document.getElementById('tableName2').innerHTML = data.matchList[data.matchIndex][3];
    document.getElementById('team1').innerHTML = data.matchList[data.matchIndex][4];
    document.getElementById('team2').innerHTML = data.matchList[data.matchIndex][5];
  }
}

function updateMatchTime(data) {
  document.getElementById('countdown').innerHTML = data.matchTimeString;
}

function handleMatchState(data) {
  if(data.matchState == 5 || data.matchState == 6) {
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
  if(data.playSound == 'abortMatch') {
    new Audio('/sounds/match_abort.mp3').play();
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
