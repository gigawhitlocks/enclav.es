/* jshint strict: true */
/* globals console */

var sendchat = (function() {
	var connection = new WebSocket('ws://'+window.location.host+window.location.pathname+'/chatws');

	connection.onopen = function(){
		console.log("Connection opened!");
	};

	connection.onclose = function(){
		console.log("Connection closed");
	};

	connection.onerror = function() {
		console.log("Error detection");
	};
	connection.onmessage = function(e){
		if ( e !== undefined ) {
			var message = JSON.parse(e.data);
			switch ( message.type ){
				case "join":
					$("#chatbox").append("<i><span style=\"color:green\">"+message.user+" has joined the room.</span></i><br />");
					break;
				case "part":
					$("#chatbox").append("<i><span style=\"color:green\">"+message.user+" has left the room.</span></i><br />");
					break;
				case "chat":
					$("#chatbox").append("<strong>"+message.user + ":</strong> " + message.message + "<br />");
					break;
				default:
					console.log("Malformed message from server \""+message+"\"");
			}
		}
	};

	return connection.send.bind(connection);
}());
