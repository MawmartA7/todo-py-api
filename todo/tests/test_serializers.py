from typing import cast

from django.test import TestCase
from ..utils.date_utils import format_datetime_to_response_date

from ..serializers import  TaskCreateSerializer, TaskListSerializer, TaskDetailAndUpdateSerializer
from ..models import Task
from django.contrib.auth.models import User


class TaskCreateSerializerUnitTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="test-user",password="test-pwd")
        self.task = Task.objects.create(
                owner=self.user,
                title=f"Task Test",
                description="Task test description",
                priority=2
        )
        self.valid_data = {
                "title": "new test task",
                "description": "new test task description",
                "priority": 1,
        }
        
    def test_serialize_model_instance(self):
        serialize = TaskCreateSerializer(self.task)
        data = cast(dict, serialize.data)
        self.assertEqual(data["title"], "Task Test")
        self.assertEqual(data["description"], "Task test description")
        self.assertEqual(data["priority"], 2)

    def test_deserialize_and_validate(self):
        serialize = TaskCreateSerializer(data=self.valid_data)
        self.assertTrue(serialize.is_valid(), serialize.errors)
        task = cast(Task, serialize.save(owner=self.user))
        self.assertEqual(task.title, self.valid_data["title"])
        self.assertEqual(task.priority, self.valid_data["priority"])

    def test_deserialize_invalid_no_title(self):
        invalid_data = {"description": "No title"}
        serialize = TaskCreateSerializer(data=invalid_data)
        self.assertFalse(serialize.is_valid())
        self.assertIn("title", serialize.errors)

    def test_deserialize_invalid_title_too_long(self):
        invalid_data = {"title": "a" * 101,"description": "title too long"}
        serialize = TaskCreateSerializer(data=invalid_data)
        self.assertFalse(serialize.is_valid())
        self.assertIn("title", serialize.errors)

    def test_deserialize_invalid_title_type(self):
        invalid_data = {"title": {"invalid":418}, "description": "invalid title type"}
        serialize = TaskCreateSerializer(data=invalid_data)
        self.assertFalse(serialize.is_valid())
        self.assertIn("title", serialize.errors)
         
    def test_deserialize_description_optional(self):
        invalid_data = {"title": "optionality of description"}
        serialize = TaskCreateSerializer(data=invalid_data)
        self.assertTrue(serialize.is_valid())
        self.assertNotIn("description", serialize.errors)
    
    def test_deserialize_invalid_description_too_long(self):
        invalid_data = {"title": "Description extremily long","description": "a" * 301}
        serialize = TaskCreateSerializer(data=invalid_data)
        self.assertFalse(serialize.is_valid())
        self.assertIn("description", serialize.errors)

class TaskDetailAndUpdateSerializerUnitTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="test-user",password="test-pwd")
        self.task = Task.objects.create(
                owner=self.user,
                title=f"Task Test",
                description="Task test description",
                priority=2
        )
        self.valid_data = {
                "title": "new test task",
                "description": "new test task description",
                "priority": 1,
        }
        
    def test_serialize_model_instance(self):
        serialize = TaskDetailAndUpdateSerializer(self.task)
        data = cast(dict, serialize.data)
        self.assertEqual(data["title"], "Task Test")
        self.assertEqual(data["description"], "Task test description")
        self.assertEqual(data["priority"], 2)

    def test_deserialize_and_validate(self):
        serialize = TaskDetailAndUpdateSerializer(data=self.valid_data)
        self.assertTrue(serialize.is_valid(), serialize.errors)
        task = cast(Task, serialize.save(owner=self.user))
        self.assertEqual(task.title, self.valid_data["title"])
        self.assertEqual(task.priority, self.valid_data["priority"])

    def test_deserialize_invalid_data(self):
        invalid_data = {"description": "No title"}
        serialize = TaskDetailAndUpdateSerializer(data=invalid_data)
        self.assertFalse(serialize.is_valid())
        self.assertIn("title", serialize.errors)
  
  
class TaskListSerializerUnitTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="test-user",password="test-pwd")
        self.tasks = []
        self.tasks_created = []
        
        for task_id in range(3):
            task_created = Task.objects.create(
                owner=self.user,
                title=f"Task Test {task_id}",
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
            
            self.tasks_created.append(task_created)
 
    def test_serialize_model_instance(self):
        serialize = TaskListSerializer(self.tasks_created, many=True)
        data = cast(list, serialize.data)
        self.assertEqual(data[1]["title"], self.tasks[1]["title"])
        self.assertEqual(data[1]["description"], self.tasks[1]["description"])
        self.assertEqual(data[1]["priority"], self.tasks[1]["priority"])
        
    def test_serialize_model_instance_with_empty_list(self):
        serialize = TaskListSerializer([], many=True)
        data = cast(list, serialize.data)
        self.assertEqual(data, [])
        