from django.db import models
from django.contrib.auth.models import User, UserManager

from django.core.urlresolvers import reverse

# Create your models here.


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

    archive = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('lobby', kwargs={"pk": self.pk})


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
    
    current_day   = models.IntegerField(default=1)
    current_state = models.CharField(max_length=15, choices=STATE)




class Vote(models.Model):
    player_voted_at = models.ForeignKey('Player', related_name="voted_at")
    player_voted    = models.ForeignKey('Player', related_name="voted")

    day             = models.ForeignKey('Day', related_name="votes")
    
