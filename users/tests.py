from django.test import TestCase
from .models import User
# Create your tests here.
from django.contrib import auth
from main.models import Role

class AuthTestCase(TestCase):
    def setUp(self):
        r = Role.objects.create(name='testrole')
        r.save()
        self.u = User.objects.create_user('test@dom.com', 'test@dom.com', 'pass', age=50, role_id=r.id)
        self.u.is_staff = True
        self.u.is_superuser = True
        self.u.is_active = True
        self.u.save()

        

    def testLogin(self):
        self.client.login(username='test@dom.com', password='pass')