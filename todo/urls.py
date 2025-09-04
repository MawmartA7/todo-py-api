from django.urls import path

from . import views

urlpatterns = [
    path('', views.TaskListCreateApiView.as_view(), name="list create tasks"),
    path('<int:pk>/', views.TaskDetailUpdateDeleteView.as_view(), name="detail update delete tasks"),
]