from django.test import TestCase, Client
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_view(self):
        # Define a dictionary with the user data
        user_data = {
            'email': 'silemnabib@gmail.com',
            'first_name': 'silem',
            'last_name': 'villa',
            'password': 'password123'
        }

        # Use the client to make a post request
        response = self.client.post('/api/signup/', user_data)

        # Check that the response has a status code of 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the data in the response is the same as the data that was posted
        self.assertEqual(response.data, UserSerializer(User.objects.get(email='silemnabib@gmail.com')).data)