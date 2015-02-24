from django.db import models
from Match.py import Match
import random

class User(models.Model):
    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=15, null=True)
    validation = models.IntegerField();

    def __str__(self):
        return self.email

    @classmethod
    def create(cls, email, username):
        user = cls(email=email, username=username, validation=random.randint(1000,9999))
        cls.save()
        return user

    @classmethod
    def validate(cls, vN):
        if (cls.validation == vN):
            cls.validation = 0
            cls.save()
            return True
        else:
            return False

    @classmethod
    def acceptMatch(cls, match):
        return match.accept(cls)

    @classmethod
    def createMatch(cls, user):
        match = Match.create(self, user)
        
