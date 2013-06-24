/* jshint strict: true */
/* globals console */

;(function() {
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
		console.log(e.data);
	};
}());
