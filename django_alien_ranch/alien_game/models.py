from django.db import models
from django.contrib.auth.models import User
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
                ('abducted', 'Abducted')
             )

    game = models.ForeignKey('Game')
    side = models.CharField(max_length=15, choices=SIDE)
    role = models.CharField(max_length=15, choices=ROLES) # go and count out max_length later :P

    current_status = models.CharField(max_length=15, choices=STATUS, default='alive')


class Game(models.Model):
    """
    The Game model represents the collection of Players who are all
    part of the same game.
    """

    created = models.DateTimeField(auto_now_add=True)
    archive = models.BooleanField(default=False)


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

    current_day   = models.IntegerField(default=1)
    current_state = models.CharField(max_length=15, choices=STATE)



class Vote(models.Model):
    player_voted_at = models.ForeignKey('Player')
    player_voted_on = models.ForeignKey('Player')

    day = models.ForeignKey('Day', related_name="votes")