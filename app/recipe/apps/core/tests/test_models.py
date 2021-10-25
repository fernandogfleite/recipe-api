from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelsTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Testa a criação se a criação de
            um novo usuário com email foi um sucesso"""

        email = "test@fernando.com"
        password = "testpass123"
        User = get_user_model()

        user = User.objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Testa se o email de um novo usuário é normalizado"""

        email = "test@FERNANDO.COM"
        User = get_user_model()
        user = User.objects.create_user(
            email=email,
            password='test123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Testa se a criação de um novo usuário sem email gera um erro"""

        with self.assertRaises(ValueError):
            User = get_user_model()
            User.objects.create_user(
                email=None,
                password='test123'
            )

    def test_create_new_superuser(self):
        """Testa a criação de um superusuário"""
        User = get_user_model()
        user = User.objects.create_superuser(
            email='test@fernando.com',
            password='test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
