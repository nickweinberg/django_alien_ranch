from django.test import TestCase
from alien_game.models import Day, Player, Game, Vote
from django.contrib.auth.models import User, UserManager
from .game import start_game
from django.db.models import Count

from random import randint, choice

from django.shortcuts import get_object_or_404

class FunTestCase(TestCase):
    def setUp(self):
        # Create some users
        User.objects.create_user(username="Nick")
        User.objects.create_user(username="Steven")
        User.objects.create_user(username="Cyrus")
        User.objects.create_user(username="Edaan")
        User.objects.create_user(username="Bob")

        # Get user List
        user_list = User.objects.all()

        # Create a game
        Game.objects.create()
        game      = Game.objects.get(pk=1)





    def test_check_if_users_exist(self):
        """test run through of entire game logic."""
        user_list = User.objects.all()
        game      = Game.objects.get(pk=1)

        # Add 5 players to the game
        for user in user_list:
            new_player = Player(user=user, game=game)
            new_player.save()

        # assert that players_list has 5 people
        players_list = game.players.all()
        self.assertEqual(players_list.count(), 5)

        SIDE        =   (
                    ('human', 'Human'),
                    ('alien', 'Alien')
                )
        # Give every user a side
        # random.randint(a, b)
        # random.choice(seq)
        for player in players_list:
            player.side = choice(SIDE)[0]
            player.save()

            print player.user, 'is a(n)', player.side



        # Game starts - Create a new Day
        new_day = Day(game=game, current_day=1, current_state='morning') # sets to morning
        new_day.save()

        # TEST: Get someone for people to vote on
        user_one   = User.objects.get(username="Bob")
        player_one = Player.objects.get(user=user_one)

        # All players make a vote
        for player_vote in players_list:
            new_vote = Vote(player_voted=player_vote, player_voted_at=player_one, day=new_day)
            new_vote.save()

        vote_list = Vote.objects.filter(day=new_day)

        # Create a hashmap of all the votes to see who got the most
        # There is probably a better way to do this
        # Ex: Output {u'Nick': 5, u'Steven': 1}
        vote_counter = {}
        for vote in new_day.votes.all():
            if vote_counter.has_key(vote.player_voted_at.user.username):
                vote_counter[vote.player_voted_at.user.username] += 1
            else:
                vote_counter[vote.player_voted_at.user.username] = 1

        player_to_be_killed = Player.objects.get(user__username=(max(vote_counter, key=vote_counter.get)))

        print player_to_be_killed.user, "got killed."

        # Set that player to dead then advance the round
        player_to_be_killed.current_status = 'dead'
        player_to_be_killed.save()
        



