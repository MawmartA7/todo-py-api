from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils.date_utils import format_datetime_to_response_date
from datetime import datetime, timedelta, timezone

from django.contrib.auth.models import User
from ..models import Task

from django.urls import reverse
from rest_framework import status

class TaskListAPITest(APITestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user(username="test-user",password="test-pwd")
        self.outher_user = User.objects.create_user(username="test-outher-user",password="test-pwd")
        self.user_token = str(RefreshToken.for_user(self.user).access_token)
        self.outher_user_token = str(RefreshToken.for_user(self.outher_user).access_token)
        
        self.tasks = []
        
        for task in range(3):
            task_created = Task.objects.create(
                owner=self.user,
                title=f"Task Test {task}",
                description="Task test description",
                priority=2
            )
            
            self.tasks.append( {
                "id": task_created.pk,
                "title": task_created.title,
                "description": task_created.description,
                "priority": task_created.priority,
                "completed": task_created.completed,
                "created_at": format_datetime_to_response_date(task_created.created_at)
            })
            
        self.url = reverse('list create tasks')
        
    def test_get_tasks_success(self):
        
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertListEqual(response.json(), self.tasks)
        
    def test_get_tasks_empty(self):
        
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.outher_user_token}")
        
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(len(response.json()) == 0)
    
    def test_get_tasks_unauthorized(self):
                
        response = self.client.get(self.url)
        
        self.assertTrue(response.status_code == status.HTTP_401_UNAUTHORIZED)
    
    def test_create_task_success(self):
        
        task = {
                "title": "new test task",
                "description": "new test task description",
                "priority": 1,
            }
        
        response = self.client.post(self.url, task, HTTP_AUTHORIZATION=f"Bearer {self.outher_user_token}")
        
        task['id'] = len(self.tasks) + 1
        
        self.assertTrue(response.status_code == status.HTTP_201_CREATED)
        self.assertEqual(response.json(), task)
        
    def test_create_invalid_task(self): 
        
        task = {
                "description": "new test task description",
                "priority": 1,
            }
        
        expected = {
            "title": [
                "Este campo é obrigatório."
            ]
        }
        
        response = self.client.post(self.url, task, HTTP_AUTHORIZATION=f"Bearer {self.outher_user_token}")

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected)
        
    def test_create_task_unauthorized(self):
        task = {
                "title": "new test task",
                "description": "new test task description",
                "priority": 1,
            }
        
        response = self.client.post(self.url, task,)
        
        self.assertTrue(response.status_code == status.HTTP_401_UNAUTHORIZED)
        
        
class TaskRetriveUpdateDeleteAPITest(APITestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user(username="test-user",password="test-pwd")
        self.outher_user = User.objects.create_user(username="test-outher-user",password="test-pwd")
        self.user_token = str(RefreshToken.for_user(self.user).access_token)
        self.outher_user_token = str(RefreshToken.for_user(self.outher_user).access_token)

        created_task = Task.objects.create(
                owner=self.user,
                title=f"Task Test 1",
                description="Task test description",
                priority=2
        )
        
        self.task = {
                "id": created_task.pk,
                "title": created_task.title,
                "description": created_task.description,
                "priority": created_task.priority,
                "completed": created_task.completed,
                "created_at": format_datetime_to_response_date(created_task.created_at),
                "updated_at": format_datetime_to_response_date(created_task.updated_at)
            }

        self.url = reverse('detail update delete tasks', kwargs={"pk": created_task.pk})
        self.url_id_not_found = reverse('detail update delete tasks', kwargs={"pk": 30})

    def test_retrive_task_success(self):
        
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertEqual(response.json(), self.task)
    
    def test_retrive_task_not_found(self):
        
        response = self.client.get(self.url_id_not_found, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)
    
    def test_retrive_task_unauthorized(self):
            
        response = self.client.get(self.url)

        self.assertTrue(response.status_code == status.HTTP_401_UNAUTHORIZED)

    def test_update_task_success(self):
        
        task = {
                "title": "new test task",
                "priority": 2
            }
        
        response = self.client.patch(self.url, task, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        almost_updated_at = datetime.now(timezone.utc)

        updated_at = response.json()["updated_at"]

        del response.json()["updated_at"]
        del self.task["updated_at"]
        
        task = self.task | task
        
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertEqual(response.json(), task)
        self.assertTrue(abs((datetime.fromisoformat(updated_at)) - almost_updated_at) < timedelta(seconds=2))
        
    def test_update_invalid_task(self): 
        
        response = self.client.patch(self.url, {}, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        almost_updated_at = datetime.now(timezone.utc)
        
        updated_at = response.json()["updated_at"]
        
        del response.json()["updated_at"]
        del self.task["updated_at"]
        
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertEqual(response.json(), self.task)
        self.assertTrue(abs((datetime.fromisoformat(updated_at)) - almost_updated_at) < timedelta(seconds=2))
    
    def test_update_task_not_found(self):
        
        task = {
                "title": "new test task",
                "priority": 2
            }
        
        response = self.client.patch(self.url_id_not_found, task, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)
    
    def test_update_task_unauthorized(self):
        
        task = {
                "title": "new test task",
                "priority": 2
            }
        
        response = self.client.patch(self.url, task)

        self.assertTrue(response.status_code == status.HTTP_401_UNAUTHORIZED)

    def test_delete_task_success(self):
        
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        self.assertTrue(response.status_code == status.HTTP_204_NO_CONTENT)
        
    def test_delete_task_not_found(self):
        
        response = self.client.delete(self.url_id_not_found, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)
    
    def test_delete_task_unauthorized(self):
        
        response = self.client.patch(self.url)

        self.assertTrue(response.status_code == status.HTTP_401_UNAUTHORIZED)
