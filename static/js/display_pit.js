var socket;

function updateRankings(data) {
  var table = document.getElementById('rankingsTable');
  var row;
  var cell;

  while(table.rows.length > 1) {
    table.deleteRow(1);
  }

  for(r=0; r<data.rankings.length; r++) {
    row = table.insertRow(r+1);
    row.insertCell(0).innerHTML = data.rankings[r][0];
    row.insertCell(1).innerHTML = data.rankings[r][1];
    row.insertCell(2);
    if(data.rankings[r][2] >= 0) {
      row.insertCell(3).innerHTML = data.rankings[r][2];
    }
    else {
      row.insertCell(3).innerHTML = 0;
    }
  }
}

function updateMatchSchedule(data) {
  var table = document.getElementById('matchScheduleTable');
  var row;
  var cell;

  updateTableList(data.tableList);
  var tablesRow = document.getElementById('tableListHeader').rows[0];

  for(m=0; m<data.matchList.length; m++) {
    row = table.insertRow(m);
    row.insertCell(0).innerHTML = data.matchList[m].matchNumber;
    row.insertCell(1).innerHTML = data.matchList[m].matchTime;
    for(c=2; c<tablesRow.cells.length; c++) {
      row.insertCell(c).innerHTML = "t";
    }
  }
}

function updateTableList(tableList) {
  var table = document.getElementById('tableListHeader');
  var row = table.rows[0];
  var cell;

  for(c=0; c<tableList.length; c++) {
    cell = row.insertCell(c+2);
    cell.innerHTML = tableList[c];
  }
}

function animate() {
  setTimeout(function() {
    $.when(
      $('#matchScheduleTable').animate({opacity: '0'}, 1000)
    ).done(function() {
      $('#curtain').animate({top: '-10', bottom: '-10', left: '-10', right: '-10'}, 500);
    });
  }, 2000);
}

$(function() {
  socket = new CheesyWebsocket('/display_pit/websocket', {
      matchList: function(event) { updateMatchSchedule(event.data) },
      rankings: function(event) { updateRankings(event.data) }
  });
});
