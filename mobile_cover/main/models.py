from django.db import models


class Cover(models.Model):
    """
    Class used to define a coord cover status.
    Objects have operator names, coords, and
    coverage type
    """

    operator = models.CharField(max_length=20)
    x = models.FloatField(max_length=30)
    y = models.FloatField(max_length=30)
    G2 = models.BooleanField()
    G3 = models.BooleanField()
    G4 = models.BooleanField()

    def __repr__(self):  # returns print string
        return (
            f"{self.operator} {self.x} {self.y}"
            f" {self.G2} {self.G3} {self.G4}"
        )
