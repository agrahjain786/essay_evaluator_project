from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class EssayTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    content = models.TextField()
    spelling_errors = models.IntegerField()
    relevant_content = models.BooleanField()
    score = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.title}'