from .models import Task
from .serializers import TaskListSerializer, TaskCreateSerializer, TaskDetailAndUpdateSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

class TaskListCreateApiView(generics.ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['completed', 'priority']

    def get_queryset(self): # type: ignore
        owner = self.request.user        
        return Task.objects.filter(owner=owner)
    
    def get_serializer_class(self): # type: ignore
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskListSerializer
        
    def perform_create(self, serializer: TaskCreateSerializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        else:
            print(serializer.errors)

class TaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = TaskDetailAndUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self): # type: ignore
        owner = self.request.user        
        return Task.objects.filter(owner=owner)