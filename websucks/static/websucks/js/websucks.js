var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
// var contest_socket = new WebSocket(ws_scheme + '://' + window.location.host + "/chat/" + user_id + "/" + contest_id);
var contest_socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat/" + user_id + "/" + contest_id);

contest_socket.onmessage = function(message) {
    var data = JSON.parse(message.data);
    console.log(data);
};