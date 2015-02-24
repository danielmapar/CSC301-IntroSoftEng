from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):

    user = models.OneToOneField(User)

    age = models.PositiveSmallIntegerField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    year_of_study = models.CharField(max_length=100, blank=True, null=True)

    program = models.CharField(max_length=100, blank=True, null=True)
    degree = models.CharField(max_length=100, blank=True, null=True)

    video_games = models.BooleanField(default=False)
    books = models.BooleanField(default=False)
    music = models.BooleanField(default=False)
    sports = models.BooleanField(default=False)

    description = models.CharField(max_length=500, blank=True, null=True)

    def accept_match(self, match):
        return match.accept(self)

    def create_match(self, user):
        return Match(user1=self, user2=user, points=self.match_value(user), accepted=False)

    FIELDS = ("age", "gender", "year_of_study", "video_games", "books", "music", "sports", "program", "degree")

    def match_value(self, interests):
        ret = 0
        for field in self.FIELDS:
            if getattr(self, field) == getattr(interests, field):
                ret += 1
        return ret

    class Meta:
        verbose_name_plural = "interests"


class Match(models.Model):
    user1 = models.ForeignKey('UserProfile', related_name="u1")
    user2 = models.ForeignKey('UserProfile', related_name="u2")
    points = models.IntegerField()
    accepted = models.BooleanField(default=False)

    def accept(self, user, val):
        if user == self.user2:
            if val:
                self.save()
                return 1
            else:
                self.delete()
                return 0
        else:
            return -1

    class Meta:
        unique_together = ("user1", "user2")
        verbose_name_plural = "matches"
        ordering = ('points', )


