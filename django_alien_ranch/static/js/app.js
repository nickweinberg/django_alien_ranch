function callback(data){
  if('error' in data){
  	alert(data.error);
  } else if ('url' in data) {
  $('#game-lobby-user-list').append('GAME STARTED:' + data.url);
  } else {
  	var stuff = '<li>'+ data.user + '</li>';
  	$('#game-lobby-user-list').append(stuff);
  }
}


