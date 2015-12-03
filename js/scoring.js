var glyph = '<span class="glyphicon glyphicon glyphicon-ok-circle" aria-hidden="true"></span>';


function updateMatchList(data) {
  createTableColumns(data.tableList);
  var table = document.getElementById('matchListTable');
  var row;
  var cell;

  for (m = 0; m < data.matchList.length; m++) {
    row = table.insertRow(m + 1);

    cell = row.insertCell(0);
    cell.innerHTML = data.matchList[m].matchNumber;

    cell = row.insertCell(1);
    cell.innerHTML = data.matchList[m].matchTime;

    for (t = 0; t < table.rows[0].cells.length - 2; t++) {
      if (table.rows[0].cells[t + 2].innerHTML.includes(data.matchList[m].tables[t % 2])) {
        cell = row.insertCell(t + 2);
        cell.innerHTML = data.matchList[m].teams[t % 2];
      } else {
        cell = row.insertCell(t + 2);
      }
    }
  }
  if(table.rows.length>1) {
    addEditButtons();
  }
}

function createTableColumns(tableList) {
  var table = document.getElementById('matchListTable');
  var row = table.rows[0];
  var cell;

  for(c=0; c<tableList.length; c++) {
    cell = row.insertCell(c+2);
    cell.innerHTML = tableList[c];
  }
}

function addEditButtons() {
  var table = document.getElementById('matchListTable');
  var row;
  var cell;

  for(m=1; m<table.rows.length; m++) {
    row = table.rows[m];
    cell = row.cells[row.cells.length-1];
    cell.innerHTML = '<button type="button" class="btn btn-success btn-xs" value="' + (m-1) + '"data-toggle="modal" data-target="#myModal">Edit</button>';
  }
}

function updateCurrentMatch(data) {

}

function publishScore() {
  var matchNumber = 1;
  var team1 = 1234;
  var score1 = 100;
  var team2 = 4321;
  var score2 = 99;
  socket.send('score', {'match':matchNumber, 'team1':{'teamNumber':team1, 'score':score1}, 'team2':{'teamNumber':team2, 'score':score2}});
}

function updateScores(data) {

}

$(function() {
  socket = new CheesyWebsocket('/scoring/websocket', {
    matchList: function(event) { updateMatchList(event.data); },
    currentMatchIndex: function(event) { updateCurrentMatch(event.data); },
    scores: function(event) { updateScores(event.data); }
  });
});
