from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token


# Role status constants:
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

PORTER = 'Porter'
SUPERVISOR = 'Supervisor'
MANAGEMENT = 'Management'
ADMIN = 'Admin'

ROLE_STATUS_CHOICES = (
    (PORTER, PORTER),
    (SUPERVISOR, SUPERVISOR),
    (MANAGEMENT, MANAGEMENT),
    (ADMIN, ADMIN),
)


class CustomUser(AbstractUser):
    staff_id_number = models.CharField(max_length=10,)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_STATUS_CHOICES)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'role': user.role
        })


