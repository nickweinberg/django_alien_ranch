function callback(data){
  if('error' in data){
  	alert(data.error);
  } else if ('url' in data) {
  	var stuff = '<li> GAME STARTED: ' + data.url +'</li>'
    $('#game-lobby-user-list').append();
  } else {
  	var stuff = '<li>'+ data.user + '</li>';
  	$('#game-lobby-user-list').append(stuff);
  }
}


