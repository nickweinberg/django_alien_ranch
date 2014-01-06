


$(document).ready(function(){

	var mostRecentMessage = 0;

	function updateChatWindow(chats){

	}



	function sendMessage(){

		$.ajax({
			type: "GET",
			url: '/api01/chat/ping/?message=HELLO!&chat_id=1&last_message_received=1388790094000',
			dataType: 'json',
			success: function(g){
				console.log(g);
				console.log("SUCCESS!!!");
			},
			error: function(xhr, text, errorScript){
				console.log("FAILURE");
				console.log(text);
				console.log(errorScript);
			}
		});
	}


	function getMessages(){
		$.ajax({
			type: "GET",
			url: '/api01/chat/ping/?chat_id=1&last_message_received=' + mostRecentMessage,
			dataType: 'json',
			success: function(g){
				console.log(g);
				mostRecentMessage = g['most_recent'];
				updateChatWindow(g['messages']);
				console.log("SUCCESS!!!");
			},
			error: function(xhr, text, errorScript){
				console.log("FAILURE");
				console.log(text);
				console.log(errorScript);
			}
		});
	}
	setInterval(getMessages,500);
});