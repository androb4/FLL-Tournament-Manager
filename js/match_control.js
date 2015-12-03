var socket;

var matchControl = {
  "timerStart": "false",
  'matchReady': 'false',
  "timeString": "2:30",
  "currentMatchIndex": 0,
  "matchList": [],
  "tableList": []
};

function updateMatchList(data) {
  console.log(data)
  var table = document.getElementById("matchListTable");
  var row;
  var cell;

  while (table.rows[0].cells.length > 2) {
    table.rows[0].deleteCell(2);
  }

  while (table.rows.length > 1) {
    table.deleteRow(1);
  }

  row = table.rows[0];

  for (t = 0; t < data.tableList.length; t++) {
    cell = row.insertCell(t + 2);
    cell.innerHTML = "<b>" + data.tableList[t] + "</b>";
  }

  for (m = 0; m < data.matchList.length; m++) {
    row = table.insertRow(m + 1);

    if (m == 0)
      row.classList.add("success");

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

  updateMatchIndexSelector(data);
}

function updateTableList(tables) {
  var table = document.getElementById("matchListTable");
  var row = table.rows[0];
  var cell;

  while (row.cells.length > 3) {
    table.deleteRow(2);
  }

  for (t = 0; t < tables.length; t++) {
    cell = row.insertCell(t + 2);
    cell.innerHTML = "<b>" + tables[t] + "</b>";
  }
}

function updateMatchIndexSelector(data) {
  var select = document.getElementById("matchIndexSelect");

  select.options.length = 0;

  for (m = 0; m < data.matchList.length; m++) {
    var option = document.createElement("option");
    option.text = data.matchList[m].matchNumber;
    select.add(option);
  }
  select.selectedIndex = data.currentMatchIndex;
}

function updateMatchIndex(data) {
  document.getElementById("matchIndexSelect").selectedIndex = data.currentMatchIndex;
}

function updateMatchTime(data) {
  console.log(data);
  document.getElementById("countdown").innerHTML = data.matchTimeString;
}

function updateMatchState(data) {
  if(data.matchState == 0) {
    $("#startMatchBtn").prop("disabled", false);
  }
  else {
    $("#startMatchBtn").prop("disabled", true);
  }
  console.log(data);
}

$(function() {
  socket = new CheesyWebsocket("/match_control/websocket", {
    matchList: function(event) {
      updateMatchList(event.data);
    },
    matchTime: function(event) {
      updateMatchTime(event.data);
    },
    matchIndex: function(event) {
      updateMatchIndex(event.data);
    },
    matchState: function(event) {
      updateMatchState(event.data);
    }
  });

  $("#matchIndexSelect").change(function() {
    var s = document.getElementById("matchIndexSelect");
    matchControl["currentMatchIndex"] = s.selectedIndex;
    socket.send('updateMatchIndex', {'matchIndex':s.selectedIndex});
  });

  $("#startMatchBtn").click(function() {
    matchControl["timerStart"] = "true"
    socket.send('matchStart');
  });

  $("#resetTimerBtn").click(function() {
    socket.send('resetTimer');
  });

  function showServerResponse(txt) {
    console.log(txt);
  }
});
