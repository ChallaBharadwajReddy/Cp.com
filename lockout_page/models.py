from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class mini_lockout(models.Model):
    player1 = models.ForeignKey(User,related_name="player1",on_delete=models.CASCADE)
    player2 = models.ForeignKey(User,related_name="player2",on_delete=models.CASCADE)
    status = models.TextField(default="Prepared")
    question1 = models.TextField(default="EMPTY")
    question2 = models.TextField(default="EMPTY")
    question3 = models.TextField(default="EMPTY")
    start_time = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.status)

class ForcesId(models.Model):
    player=models.ForeignKey(User,on_delete=models.CASCADE)
    handel=models.TextField()

    def __str__(self):
        return str(self.player.username)