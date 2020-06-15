from django.contrib.auth.models import AbstractUser
from django.db import models

# Role status constants:
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
