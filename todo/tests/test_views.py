from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils.date_utils import format_datetime_to_response_date
from datetime import datetime, timedelta, timezone
import random

from django.contrib.auth.models import User
from ..models import Task

from django.urls import reverse
from rest_framework import status

DEFAULT_PAGE_SIZE: int = 10

class TaskListAPITest(APITestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user(username="test-user",password="test-pwd")
        self.outher_user = User.objects.create_user(username="test-outher-user",password="test-pwd")
        self.user_token = str(RefreshToken.for_user(self.user).access_token)
        self.outher_user_token = str(RefreshToken.for_user(self.outher_user).access_token)
        
        self.tasks_length = 14
        
        priorities = [random.randint(1, 3) for _ in range(self.tasks_length - 3)] + [1,2,3]

        self.tasks = []
        
        for task_id in range(self.tasks_length):
            task_created = Task.objects.create(
                owner=self.user,
                title=f"Task Test {task_id}",
                description="Task test description",
                priority=priorities[task_id],
                is_done=task_id % 2 == 0
            )
            
            self.tasks.append( {
                "id": task_created.pk,
                "title": task_created.title,
                "description": task_created.description,
                "priority": task_created.priority,
                "is_done": task_created.is_done,
                "created_at": format_datetime_to_response_date(task_created.created_at)
            })
        
        self.tasks.sort(key=lambda task: (task["priority"], task['created_at']), reverse=True)
        
        self.url = reverse('list create tasks')
        
    def test_get_tasks_success(self):
        
        expected = {
            "count": len(self.tasks),
            "results": self.tasks[:DEFAULT_PAGE_SIZE]
        }
        
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(response.json()["count"] == expected["count"])
        self.assertListEqual(response.json()["results"], expected["results"])
        
    def test_get_tasks_page_two_success(self):
    
        page = 2
    
        expected = {
            "count": len(self.tasks),
            "results": self.tasks[DEFAULT_PAGE_SIZE:DEFAULT_PAGE_SIZE * page]
        }
        
        response = self.client.get(self.url, data={"page":page}, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(response.json()["count"] == expected["count"])
        self.assertListEqual(response.json()["results"], expected["results"])
        
    def test_get_tasks_page_size(self):
    
        page = 2
    
        new_page_size = 4
    
        expected = {
            "count": len(self.tasks),
            "results": self.tasks[new_page_size:new_page_size * 2]
        }
        
        response = self.client.get(self.url, data={"page": page, "size": new_page_size}, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(response.json()["count"] == expected["count"])
        self.assertListEqual(response.json()["results"], expected["results"])
    
    def test_get_tasks_empty_page(self):
        
        expected = {
            "detail": "Invalid page."
        }
        
        response = self.client.get(self.url, data={"page":4}, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), expected)
   
    def test_get_tasks_filter_by_priority(self):
        
        for priority in [1,2,3]:
            response = self.client.get(self.url, data={"priority": priority}, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
            
            self.assertTrue(response.status_code == status.HTTP_200_OK)
            self.assertTrue(all(task["priority"] == priority for task in response.json()["results"]))
        
    def test_get_tasks_filter_is_done(self):    
            
        for is_done in [True,False]:
            response = self.client.get(self.url, data={"is_done": is_done}, HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
            
            self.assertTrue(response.status_code == status.HTTP_200_OK)
            self.assertTrue(all(task["is_done"] == is_done for task in response.json()["results"]))
    
    def test_get_tasks_filter_priority_and_is_done(self):
        response = self.client.get(
            self.url,
            data={"priority": 2, "is_done": True},
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}"
        )
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertTrue(all(task["priority"] == 2 and task["is_done"] is True for task in results))
     
    def test_get_tasks_empty(self):
        
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.outher_user_token}")
        
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(response.json()["count"] == 0)
        self.assertTrue(len(response.json()["results"]) == 0)
    
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

        response = self.client.post(self.url, task, HTTP_AUTHORIZATION=f"Bearer {self.outher_user_token}")

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.json())
        
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
                "is_done": created_task.is_done,
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
