from django.test import TestCase

from typing import cast

from ..serializers import UserSerializer
from django.contrib.auth.models import User


class UserSerializerUnitTest(TestCase):
    
    def test_serialize_model_instance(self):
        user = User.objects.create_user(username="user-name",password="user-pwd")
        
        serialize = UserSerializer(user)
        data = cast(dict, serialize.data)
        self.assertEqual(data["username"], "user-name")
    
    def test_deserialize_and_validate_and_save(self):
        
        valid_data = {
            "username": "user-name-2",
            "password": "user-pwd-2"
        }
        
        serialize = UserSerializer(data=valid_data)
        self.assertTrue(serialize.is_valid(), serialize.errors)
        user = cast(User, serialize.save())
        self.assertEqual(user.username, valid_data["username"])
        self.assertNotEqual(user.password, valid_data["password"], "Password not encripted.")
        self.assertTrue(user.check_password(valid_data["password"]), "Password not encripted or check_password failed.")
    
    def test_deserialize_and_update(self):
        user_to_update = User.objects.create_user(username="old-username", password="old-pwd")
    
        update_data = {
            "username": "new-username",
            "password": "new-pwd"
        }
    
        serialize = UserSerializer(instance=user_to_update, data=update_data)
        self.assertTrue(serialize.is_valid(), serialize.errors)
        
        updated_user = cast(User, serialize.save())
        
        self.assertEqual(updated_user.pk, user_to_update.pk)
        self.assertEqual(updated_user.username, "new-username")
        self.assertFalse(updated_user.check_password("old-pwd"))
        self.assertNotEqual(updated_user.password, update_data["password"], "Password not encripted.")
        self.assertTrue(updated_user.check_password("new-pwd"))
    
    def test_deserialize_invalid_no_username(self):
        invalid_data = {"password": "pwd123"}
        serialize = UserSerializer(data=invalid_data)
        self.assertFalse(serialize.is_valid())
        self.assertIn("username", serialize.errors)
           
    def test_deserialize_invalid_username_chars(self):
        invalid_data = {"username": "Invałid (char§)", "password": "pwd123"}
        serialize = UserSerializer(data=invalid_data)
        self.assertFalse(serialize.is_valid())
        self.assertIn("username", serialize.errors)
    
    def test_deserialize_invalid_username_too_long(self):
        invalid_data = {"username": "a" * 151, "password": "pwd123"}
        serialize = UserSerializer(data=invalid_data)
        self.assertFalse(serialize.is_valid())
        self.assertIn("username", serialize.errors)
    
    def test_deserialize_invalid_no_password(self):
        invalid_data = {"username": "user-name123"}
        serialize = UserSerializer(data=invalid_data)
        self.assertFalse(serialize.is_valid())
        self.assertIn("password", serialize.errors)
           
    def test_deserialize_invalid_password_too_long(self):
        invalid_data = {"username": "user-name123", "password": "a" * 129}
        serialize = UserSerializer(data=invalid_data)
        self.assertFalse(serialize.is_valid())
        self.assertIn("password", serialize.errors)
        