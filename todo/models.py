from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Task(models.Model):
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True, null=True)
    priority = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], default=1)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "tasks" 