from django.db import models

class Interests(models.Model):
    PROGRAM_CHOICES = (
        ('CS', 'Computer Science'),
        ('RC', 'Rotman Commerce'),
        ('AS', 'Arts and Science'),
        ('EG', 'Engineering'),
    )
    DEGREE_OF_STUDY = (
        ('UG', 'Undergraduate'),
        ('MA', 'Masters'),
        ('PD', 'Post-doctorate'),
        ('AL', 'Alumnus/Alumna'),
        ('PR', 'Professor'),
        ('TA', 'TA'),
    )
    FIELDS = ("videoGames", "books", "music")

    user = models.ForeignKey('User')
    program = models.CharField(max_length=2, choices=PROGRAM_CHOICES)
    degree = models.CharField(max_length=2, choices=DEGREE_OF_STUDY)

    videoGames = models.BooleanField(default=False)
    books = models.BooleanField(default=False)
    music = models.BooleanField(default=False)

    @classmethod
    def matchValue(cls, interests):
        ret = 0
        if (cls.program == interests.program):
            ret += 1
        if (cls.degree == interests.degree):
            ret += 1
        #cls._meta.get_all_field_names()
        return ret

    class Meta:
        verbose_name_plural = "interests"
