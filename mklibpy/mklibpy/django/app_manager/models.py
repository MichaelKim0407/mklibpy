from django.db import models

__author__ = 'Michael'


class App(models.Model):
    order = models.IntegerField()
    name = models.CharField(max_length=45, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}[{}] '{}'".format(
            self.__class__.__name__,
            self.order,
            self.name
        )
