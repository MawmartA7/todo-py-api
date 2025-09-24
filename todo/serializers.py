from rest_framework import serializers
from .models import Task

class TaskCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = ["id", "title", "description", "priority"]
        read_only_fields = ["id"]
        
class TaskListSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = Task
        fields = ["id", "title", "description", "priority", "is_done", "created_at"]

class TaskDetailAndUpdateSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = Task
        fields = ["id", "title", "description", "priority", "is_done", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]