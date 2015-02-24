from django.db import models

class Match(models.Model):
    user1 = models.ForeignKey('User')
    user2 = models.ForeignKey('User')
    accepted = models.BooleanField(default=False)

    @classmethod
    def create(cls, user1, user2):
        match = cls(user1=user1, user2=user2)
        match.save()
        return match
    
    @classmethod
    def accept(cls, user, val):
        if (user.id == self.user2.id):
            accepted = val
            if(val):
                cls.save()
                return 1
            else:
                cls.delete()
                return 0
        else:
            return -1

    class Meta:
        unique_together = ("user1", "user2")
        verbose_name_plural = "matches"
