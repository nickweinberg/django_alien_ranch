from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.shortcuts import render, get_object_or_404

from .models import Player, Game, Day, Chat, ChatMessage

from .forms import GameCreateForm
from django.contrib.auth.models import User

import json
from django.http import HttpResponse

import datetime

from dajaxice.decorators import dajaxice_register

from .game import start_game, morning_vote_round_resolve, night_vote_round_resolve,

# This is the short API call to send messages
def game_chat_send(request):

	# Print out the parameters we are getting
	print request.GET

	# Make sure there is a message in the request URL
	if 'message' in request.GET and 'last_message_received' in request.GET and 'chat_id' in request.GET:

		# Get the chat_id                                                     ############################     FIX THIS EVENTUALLY!
		chat = get_object_or_404(Chat, pk=request.GET['chat_id'])

		# Create a new message to save
		cm = ChatMessage(message = request.GET['message'], chat = chat)

		# Save the new message
		cm.save()

		# Get the DateTime of the last received message
		millisecs = request.GET['last_message_received']
		dt = datetime.datetime.fromtimestamp(int(millisecs)//1000)

		# Query the database for the messages received after the user's last received.
		list_of_new_chatmessages = ChatMessage.filter(chat=chat).filter(timestamp__gt=dt).order_by(timestamp).all()

		# Create a variable to save the chat message data
		output_messages = [];

		# One more variable to save the most recent messages timestamp
		most_recent = 0;

		# Make the list into a javascript-comprehensive thing
		for all_cms in list_of_new_chatmessages:
			output_messages.append({
				'timestamp': int(dt.strftime('%s')) * 1000,
				'text': all_cms.message
			})
		
		# Create the final dictionary to send to the front
		dict_to_send = {
			'success': True,
			'messages': output_messages,
		}

		return HttpResponse(simplejson.dumps(dict_to_send), mimetype='application/javascript')
	else:
		# Create the final dictionary to send to the front
		dict_to_send = {
			'success': False,
			'params': request.GET,
		}
		return HttpResponse(simplejson.dumps(dict_to_send), mimetype='application/javascript')

# This is the 'ping' api function
def game_chat_ping(request):

	# Print te parameters we are getting
	print request.GET

	# Now we make sure there is a timestamp in the message
	if 'last_message_received' in request.GET and 'chat_id' in request.GET:

		# Get the chat_id                                                     ############################     FIX THIS EVENTUALLY!
		chat = get_object_or_404(Chat, pk=request.GET['chat_id'])

		# Get the DateTime of the last received message
		millisecs = request.GET['last_message_received']

		dt = datetime.datetime.fromtimestamp(int(millisecs)//1000)

		# Query the database for the messages received after the user's last received.
		list_of_new_chatmessages = ChatMessage.objects.filter(chat=chat).filter(timestamp__gt=dt).all()

		# Create a variable to save the chat message data
		output_messages = []

		# One more variable to save the most recent messages timestamp
		most_recent = int(request.GET['last_message_received'])

		# Make the list into a javascript-comprehensive thing
		for all_cms in list_of_new_chatmessages:
			output_messages.append({
				'timestamp': int(all_cms.timestamp.strftime('%s')) * 1000,
				'text': all_cms.message
			})
			print "GOT ONE"
			if most_recent < (int(all_cms.timestamp.strftime('%s')) * 1000):
				most_recent = (int(all_cms.timestamp.strftime('%s')) + 1) * 1000

		
		# Create the final dictionary to send to the front
		dict_to_send = {
			'success': True,
			'messages': output_messages,
			'most_recent': most_recent
		}

		return HttpResponse(simplejson.dumps(dict_to_send), mimetype='application/javascript')
	else:
		# Create the final dictionary to send to the front
		dict_to_send = {
			'success': False,
			'params': request.GET,
		}
		return HttpResponse(simplejson.dumps(dict_to_send), mimetype='application/javascript')


class GameListView(ListView):
    model = Game


class GameCreateView(CreateView):
    model = Game
    form_class = GameCreateForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.save()

        return super(CreateView, self).form_valid(form)

def GameLobbyView(request, pk):
    current_game = get_object_or_404(Game, pk=pk)
    players = current_game.players.all()
    
    # dunno why i made it guest
    guest = request.user
    data = {
        'object': current_game,
        'players': players,
        'guest': guest 
        }


    return render(request, 'alien_game/game_detail.html', data)


def MainGameView(request, pk, current_day):
    current_game = get_object_or_404(Game, pk=pk)
    this_day  = get_object_or_404(Day, current_day=current_day)
    players = current_game.players.all()
    user = request.user

    object = {
        'game'       : current_game,
        'players'    : players,
        'user'       : user,
        'current_day': this_day

    }

    return render(request, 'alien_game/game_play.html', object)

