/* jshint strict: true */
/* globals console */

var sendchat = (function() {
	var connection = new WebSocket('ws://'+window.location.host+window.location.pathname+'/chatws');
	window.addEventListener("unload", connection.close);

	connection.onopen = function(){
		//TODO: query server for existing users to build the user list
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
					$("#chatbox")
						.append("<span class=\"chat_notice\">"
								+message.user+" has joined the room.</span><br />");
					$("#userlist")
						.append("<span id=\""+message.user+"_list\">"+message.user+"</span><br />");
					break;

				case "part":
					$("#chatbox")
						.append("<i><span class=\"chat_notice\">"
								+message.user+" has left the room.</span></i><br />");
					$("#userlist").remove("#"+message.user+"_list");
					break;

				case "chat":
					$("#chatbox")
						.append("<strong><span style=\"color: blue;\">" // TODO: mIRC-style username colors
								+message.user+":</strong></span> " + message.message + "<br />");
					break;

				default:
					console.log("Malformed message from server \""+message+"\"");
			}
		}
	};

	return connection.send.bind(connection);
}());
