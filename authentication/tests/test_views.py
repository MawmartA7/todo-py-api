from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework import status

class CreateUserAPITest(APITestCase):
    
    def setUp(self):
        
        self.url = reverse('register')
        
    def test_create_user_success(self):
        
        data = {
            "username": "user-name",
            "password": "user-pwd"
        }
        
        response = self.client.post(self.url, data)
        
        self.assertTrue(response.status_code == status.HTTP_201_CREATED)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["username"], data["username"])
    
    def test_create_user_already_exists(self):

        self.user = User.objects.create_user(username="test-user",password="test-pwd")
        
        data = {
            "username": "test-user",
            "password": "test-pwd"
        }
        
        response = self.client.post(self.url, data)
        
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.json())
    
    def test_create_user_invalid_username_chars(self):
        
        invalid_data = {"username": "Invałid (char§)", "password": "pwd123"}
        
        response = self.client.post(self.url, invalid_data)
        
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.json())
    
    def test_create_user_invalid_no_username(self):
        
        invalid_data = {"password": "pwd123"}
        
        response = self.client.post(self.url, invalid_data)
        
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.json())
        
    def test_create_user_invalid_username_too_long(self):
        
        invalid_data = {"username": "a" * 151, "password": "pwd123"}
        response = self.client.post(self.url, invalid_data)
        
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.json())
        
    def test_create_user_invalid_no_password(self):
        
        invalid_data = {"username": "user-name123"}
        
        response = self.client.post(self.url, invalid_data)
                
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.json())
        
    def test_create_user_invalid_password_too_long(self):

        invalid_data = {"username": "user-name123", "password": "a" * 151}
        response = self.client.post(self.url, invalid_data)

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.json())
        
class TokenObtainPairAPITest(APITestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user(username="test-user",password="test-pwd")

        self.url = reverse("login")
    
    def test_login_success(self):
        
        data = {
            "username": "test-user",
            "password": "test-pwd"
        }
        
        response = self.client.post(self.url, data)
        
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())
        
        
        self.assertFalse(response.json()["access"] == "")
        self.assertFalse(response.json()["refresh"] == "")
    
    def test_login_invalid_credentials(self):
        
        data = {
            "username": "non-existent-user",
            "password": "wrong-password"
        }
        
        response = self.client.post(self.url, data)

        self.assertTrue(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        self.assertNotIn("access", response.json())
        self.assertNotIn("refresh", response.json())
    
    def test_login_invalid_no_username(self):
        
        invalid_data = {"password": "pwd123"}
        
        response = self.client.post(self.url, invalid_data)
        
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.json())
        
    def test_login_invalid_no_password(self):
        
        invalid_data = {"username": "user-name123"}
        
        response = self.client.post(self.url, invalid_data)
                
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.json())

class TokenVerifyAPITest(APITestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user(username="test-user",password="test-pwd")

        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = self.refresh_token.access_token


        self.url = reverse("verify_token")
        
    def test_access_token_verify(self):
        
        data = {
            "token": self.access_token
        }
        
        response = self.client.post(self.url, data)
        
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        
    def test_refresh_token_verify(self):
        
        data = {
            "token": self.refresh_token
        }
        
        response = self.client.post(self.url, data)
        
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        
    def test_invalid_token_verify(self):
        
        invalid_data = {
            "token": "vAMfeCcTefLVmA2GsSLzaWdght." * 3
        }
        
        response = self.client.post(self.url, invalid_data)
        
        self.assertTrue(response.status_code == status.HTTP_401_UNAUTHORIZED)

class TokenRefreshAPITest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="test-user",password="test-pwd")

        self.refresh_token = RefreshToken.for_user(self.user)

        self.url = reverse("refresh")
        
    def test_token_refresh_success(self):
        
        data = {
            "refresh": self.refresh_token
        }
        
        response = self.client.post(self.url, data)
        
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertIn("access", response.json())
        
    
    def test_invalid_token_refresh(self):
        
        invalid_data = {
            "refresh": "vAMfeCcTefLVmA2GsSLzaWdght." * 3
        }
        
        response = self.client.post(self.url, invalid_data)
        
        self.assertTrue(response.status_code == status.HTTP_401_UNAUTHORIZED)