/* jshint strict: true */
/* globals console */

var sendmessage = (function() {
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
			console.log(message);
			$("#chatbox").append(message.user + ": " + message.message + "<br />");
		}
	};

	return connection.send.bind(connection);
}());
