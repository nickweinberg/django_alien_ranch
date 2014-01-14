from django.db import models
from django.contrib.auth.models import User, UserManager

from django.core.urlresolvers import reverse

# NOT CURRENTLY USING CHAT-CHATMESSAGE MODELS
# The chatroom associated with a single game
class Chat(models.Model):
    users = models.ManyToManyField(User,related_name="chats")

    def __unicode__(self):
        return "Chat Room"

# A single message saved in the database that is associated with a player and a chat
class ChatMessage(models.Model):
    user = models.ForeignKey(User,related_name="chat_messages", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True) 
    chat = models.ForeignKey(Chat, related_name="messages")
    message = models.TextField(max_length=2000,blank=True)

    def __unicode__(self):
        return "Chat message by " + self.user.username


# Roles for players
HUMAN_ROLES =   (
                    ('villager', 'Villager'),
                    ('sheriff', 'Sheriff' ),
                    ('doctor', 'Doctor'  ),
                    ('prospector', 'Prospector')
                )

ALIEN_ROLES =   (
                    ('alien', 'Alien'),
                    ('overlord', 'Overlord')
                )
# Combine them both:
ROLES = HUMAN_ROLES + ALIEN_ROLES

# Each player is on a side
SIDE        =   (
                    ('human', 'Human'),
                    ('alien', 'Alien')
                )


class Player(models.Model):
    """
    The player models represents the individual Player in the 
    Game. They can be on the Human side or the Alien side.

    Human side can have roles: Villager, Sheriff, Doctor, Prospector.
    Alien side can have roles: Alien, Overlord.

    A Player has a status: Alive, Abducted
    """
    STATUS = (
                ('alive', 'Alive'),
                ('dead', 'Dead')
             )

    user = models.ForeignKey(User, related_name='players')
    game = models.ForeignKey('Game', related_name='players')
    
    # Decided at gametime *TOUCHDOWN*
    side = models.CharField(max_length=15, choices=SIDE, default='human')
    role = models.CharField(max_length=15, choices=ROLES, default='villager') # go and count out max_length later :P

    current_status = models.CharField(max_length=15, choices=STATUS, default='alive')


class Game(models.Model):
    """
    The Game model represents the collection of Players who are all
    part of the same game.
    """
    users = models.ManyToManyField(User, related_name="games", through="Player")
    created = models.DateTimeField(auto_now_add=True)
    has_started = models.BooleanField(default=False)
    num_of_aliens = models.IntegerField(default=1)

    archive = models.BooleanField(default=False)
    winner  = models.CharField(max_length=15, choices=SIDE, blank=True)

    def get_absolute_url(self):
        return reverse('lobby', kwargs={"pk": self.pk})

    def get_alive_player_count(self):
        return self.players.filter(current_status='alive').count()

    def get_alive_players(self):
        return self.players.filter(current_status='alive')

    def get_alive_alien_count(self):
        return self.players.filter(current_status='alive', side='alien').count()

    def get_alive_aliens(self):
        return self.players.filter(current_status='alive', side='alien')

    def get_alive_humans(self):
        return self.players.filter(current_status='alive', side='human')

    def get_alive_human_count(self):
        return self.players.filter(current_status='alive', side='human').count()

    def check_game_over(self):
        if self.get_alive_alien_count() == 0:
            self.winner = SIDE[0][0]
            self.archive = True
            self.save()
            return True
        elif self.get_alive_alien_count() >= self.get_alive_human_count():
            self.winner = SIDE[1][0]
            self.archive = True
            self.save()
            return True
        # game isn't over
        return False

    def latest_day(self):
        return self.days.latest('current_day')



class Day(models.Model):
    """
    The Day model stores the state of the game for the current
    Day. When game first starts it is Day 1.
    Each day can either be Morning or Night.
    """

    STATE = (
                ('morning', 'Morning'),
                ('night', 'Night')
            )


    game          = models.ForeignKey(Game, related_name="days")
    message       = models.TextField(max_length=200)
    current_day   = models.IntegerField(default=1) # Maybe this should be day_of_game to be more clear
    current_state = models.CharField(max_length=15, choices=STATE)

    def set_to_night(self):
        self.current_state = self.STATE[1][0]
        self.save()

    def did_everyone_vote_day(self):
        if self.votes.count() >= self.game.get_alive_player_count():
            return True
        else:
            return False

    def did_everyone_vote_night(self):
        if self.votes.filter(vote_time='night').count() >= self.game.get_alive_alien_count():
            return True
        else:
            return False

    def set_day_message(self):
        # Not using this right now

        # if it's first day WELCOME
        if self.current_day == 1:
            selfmessage == "DAY 1: Welcome!"

    def count_up_votes(self, vote_time):
        # Create a hashmap of all the votes to see who got the most
        # There is probably a better way to do this
        # Ex: Output {u'Nick': 5, u'Steven': 1}
        is_no_ties = None
        vote_counter = {}
        for vote in self.votes.filter(vote_time=vote_time):
            if vote_counter.has_key(vote.player_voted_at.user.username):
                vote_counter[vote.player_voted_at.user.username] += 1
            else:
                vote_counter[vote.player_voted_at.user.username] = 1
        
        # check if there are any ties
        v = vote_counter.values()
        for i in xrange(len(v) - 2):
            if cmp(v[i], v[i+i]):
                is_no_ties = False
                player_to_be_killed = None

        if not is_no_ties:
            is_no_ties = True
            # this gives ValueError: max() arg is an empty sequence if there are no aliens
            # but game should be over in that case!!
            player_to_be_killed = Player.objects.get(user__username=(max(vote_counter, key=vote_counter.get)), game=self.game)
    
        return is_no_ties, player_to_be_killed

    def create_new_day(self, game_obj, message):
        # message is what's displayed at the top for the new day
        # is usually who died the night before and role specific messages

        new_day = Day(game=game_obj, message=message, current_day=self.current_day + 1)
        new_day.save()

        return new_day

    def get_absolute_url(self):
        return reverse('play', kwargs={"pk": self.game.pk, "current_day": self.current_day})




class Vote(models.Model):
    STATE = (
                ('morning', 'Morning'),
                ('night', 'Night')
        )

    player_voted_at = models.ForeignKey('Player', related_name="voted_at")
    player_voted    = models.ForeignKey('Player', related_name="voted")
    vote_time       = models.CharField(max_length=15, choices=STATE, default=STATE[0][0])

    day             = models.ForeignKey('Day', related_name="votes")

    def save(self, *args, **kwargs):
        # CHECK IF PLAYER_VOTED EXISTS
        if not self.day.votes.filter(player_voted=self.player_voted, vote_time=self.day.current_state).exists():

            # correctly sets vote_time
            self.vote_time=self.day.current_state
            super(Vote, self).save(*args, **kwargs) # Call the "real" save() method.
    
