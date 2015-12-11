var glyph = '<span class="glyphicon glyphicon glyphicon-ok-circle" aria-hidden="true"></span>';
var matchList;

function updateMatchList(data) {
  matchList = data.matchList;
  var table = document.getElementById('matchListTable');
  var row;
  var cell;

  while (table.rows[0].cells.length > 4) {
    table.rows[0].deleteCell(2);
  }

  while (table.rows.length > 1) {
    table.deleteRow(1);
  }

  createTableColumns(data.tableList);

  for (m = 0; m < data.matchList.length; m++) {
    row = table.insertRow(m + 1);

    cell = row.insertCell(0);
    cell.innerHTML = data.matchList[m][0];

    cell = row.insertCell(1);
    cell.innerHTML = data.matchList[m][1];

    for (t = 0; t < table.rows[0].cells.length - 2; t++) {
      if (table.rows[0].cells[t + 2].innerHTML == data.matchList[m][2]) {
        cell = row.insertCell(t + 2);
        cell.innerHTML = data.matchList[m][4];
      }
      else if (table.rows[0].cells[t + 2].innerHTML == data.matchList[m][3]) {
        cell = row.insertCell(t + 2);
        cell.innerHTML = data.matchList[m][5];
      } else {
        cell = row.insertCell(t + 2);
      }
    }
  }
  if(table.rows.length>1) {
    addEditButtons(data);
  }
}

function createTableColumns(tableList) {
  var table = document.getElementById('matchListTable');
  var row = table.rows[0];
  var cell;

  for(c=0; c<tableList.length; c++) {
    cell = row.insertCell(c+2);
    cell.innerHTML = tableList[c][1];
  }
}

function addEditButtons(data) {
  var table = document.getElementById('matchListTable');
  var row;
  var cell;

  for(m=1; m<table.rows.length; m++) {
    row = table.rows[m];
    cell = row.cells[row.cells.length-1];
    if(data.matchList[m-1][6] == 0) {
      cell.innerHTML = '<button type="button" class="btn btn-success btn-xs" data-match-index="' + (m-1) + '"data-toggle="modal" data-target="#editScoreModal">Edit</button>';
    }
    else {
      cell.innerHTML = '<button type="button" class="btn btn-danger btn-xs" data-match-index="' + (m-1) + '"data-toggle="modal" data-target="#editScoreModal">Edit</button>';
    }
  }
}

function updateCurrentMatch(data) {

}

function publishScore() {
  var matchNumber = $('#editScoreModal').find('#matchNumber').text();
  var team1 = $('#editScoreModal').find('#team1').text();
  var score1 = $('#editScoreModal').find('#score1').val();
  var team2 = $('#editScoreModal').find('#team2').text();
  var score2 = $('#editScoreModal').find('#score2').val();
  if(score1 != '' && score2 != '') {
    socket.send('score', {'match':matchNumber, 'team1':{'teamNumber':team1, 'score':score1}, 'team2':{'teamNumber':team2, 'score':score2}});
    $('#editScoreModal').modal('hide');
  }
}

function updateScores(data) {

}

$(function() {
  socket = new CheesyWebsocket('/scoring/websocket', {
    matchList: function(event) { updateMatchList(event.data); },
    currentMatchIndex: function(event) { updateCurrentMatch(event.data); },
    scores: function(event) { updateScores(event.data); }
  });

  $('#editScoreModal').on('show.bs.modal', function (event) {
    console.log(matchList);
    var button = $(event.relatedTarget); // Button that triggered the modal
    var matchNumber = button.data('match-index')+1; // Extract info from data-* attributes
    var modal = $(this);
    modal.find('#matchNumber').text(matchNumber);
    modal.find('#team1').text(matchList[matchNumber-1][4]);
    modal.find('#team2').text(matchList[matchNumber-1][5]);
  });

  $('#publishScore').click(function() {
    publishScore();
  });
});
