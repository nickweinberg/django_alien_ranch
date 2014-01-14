from django.test import TestCase
from alien_game.models import Day, Player, Game, Vote
from django.contrib.auth.models import User, UserManager
from .game import start_game, morning_vote_round_resolve, night_vote_round_resolve
from django.db.models import Count

from random import randint, choice

from django.shortcuts import get_object_or_404

# GOTTA WRITE REAL TESTS

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


    # not running this one atm
    def woah_test_game_logic(self):
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
        # set everyone to human
        for player in players_list:
            player.side = SIDE[0][0]
            player.save()

        # Pick random guy, make him alien
        alien_guy = choice(players_list)
        alien_guy.side = SIDE[1][0]
        alien_guy.save()


        # make dict just for testing, i want to see if roles are correct.
        side_dict = {}
        for player in players_list:
            side_dict[player.user] = player.side

        print side_dict

        # Game starts - Create a new Day
        new_day = Day(game=game, current_day=1, current_state='morning') # sets to morning
        new_day.save()

        # TEST: Get someone for people to vote on
        user_one   = User.objects.get(username="Bob")
        player_one = Player.objects.get(user=user_one)


        # All players make a vote
        for player_vote in players_list:
            new_vote = Vote(player_voted=player_vote, player_voted_at=choice(players_list), day=new_day)
            new_vote.save()

        vote_list = Vote.objects.filter(day=new_day)

        self.assertEqual(new_day.did_everyone_vote_day(), True)
        
        is_no_ties, player_to_be_killed = new_day.count_up_votes('morning')
        print player_to_be_killed.user, "got killed. And is a(n)", player_to_be_killed.side

        if is_no_ties:
            # Set that player to dead
            player_to_be_killed.current_status = 'dead'
            player_to_be_killed.save()
        elif not is_no_ties:
            # There was a tie, no one dies
            pass

        print 'There are', game.get_alive_alien_count(), 'aliens left!'
        # check if game is over (no more aliens left)
        if game.get_alive_alien_count() <= 0:
            game.check_game_over()

        # then advance the round
        new_day.set_to_night()

        # now the aliens vote
        alien_list = game.get_alive_aliens()
        human_list = game.get_alive_humans()

        for alien in alien_list:
            alien_vote = Vote(player_voted=player_vote, player_voted_at=choice(human_list), day=new_day, vote_time='night')
            alien_vote.save()


        print 'Did every alien vote?', new_day.did_everyone_vote_night()

        # figure out who died
        is_no_ties, player_to_be_killed = new_day.count_up_votes('night')

        if is_no_ties:
            # Set that player to dead
            player_to_be_killed.current_status = 'dead'
            player_to_be_killed.save()
        elif not is_no_ties:
            # There was a tie, no one dies
            pass

        # Make a new instance of day
        night_message = str(player_to_be_killed.user) + " got abducted!"

        
        another_day = new_day.create_new_day(game, night_message)

        print another_day.message

    def test_full_run_through(self):
        
        # get 5 users and game
        user_list = User.objects.filter(pk__in=[1,2,3,4,5])
        game      = Game.objects.get(pk=1)

        for user in user_list:
            new_player = Player(user=user, game=game)
            new_player.save()
            if Player.objects.filter(game=game).count() == 5:
                start_game(game)

        # Assert that players list has 5 people
        players_list = game.players.all()
        self.assertEqual(players_list.count(), 5)

        # Assert that game has one day Day 1
        self.assertEqual(game.days.count(), 1)

        # Assert that current game day is 1
        self.assertEqual(game.days.all()[0].current_day, 1)
        self.assertEqual(game.days.all()[0].current_state, 'morning')

        # Assert that there is one alien and 4 players
        self.assertEqual(game.get_alive_alien_count(), 1)
        self.assertEqual(game.get_alive_human_count(), 4)

        # go through an each player makes a vote
        # checks each time if everyone voted
        d1 = Day.objects.get(game=game, current_day=1)

        for player in players_list:
            new_vote = Vote(player_voted=player, player_voted_at=choice(players_list), day=d1)
            new_vote.save()
            if d1.did_everyone_vote_day():
                morning_vote_round_resolve(game, d1)

        # assert that everyone did vote
        self.assertEqual(d1.did_everyone_vote_day(), True)
        self.assertEqual(d1.current_state, 'night')

        
        alien_list = game.get_alive_aliens()
        # curious about abducted players
        dead_players = Player.objects.filter(game=game, current_status='dead')
        for dead_guy in dead_players:
            print dead_guy.user, 'is dead.'

        # assert that aliens > 0
        self.assertTrue(len(alien_list) > 0)

        # assert that we have one dead guy
        self.assertTrue(len(dead_players) == 1)

        for alien in alien_list:
            new_vote = Vote(player_voted=alien, player_voted_at=choice(players_list), day=d1)
            new_vote.save()
            if d1.did_everyone_vote_night():
                night_vote_round_resolve(game, d1)


        self.assertEqual(Vote.objects.filter(day=d1, vote_time='night').count(), 1)
    
        # assert latest day is Day 2
        self.assertEqual(game.latest_day().current_day, 2)

        d2 = game.latest_day()
        print d2.message
        



