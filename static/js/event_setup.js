var socket;

$(function() {

  socket = new CheesyWebsocket('/event_setup/websocket', {
      matchList: function(event) { updateMatchSchedule(event.data) }
  });

  $('#clearDtabaseButton').click(function() {
    socket.send('database', {'cmd':'clearDatabase'});
  });
});
