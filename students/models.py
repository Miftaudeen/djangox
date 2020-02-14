from django.db import models

SEX_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
    ('Unknown', 'Unknown'),
)

# Create your models here.
class Student(models.Model):
    matric_num = models.CharField(max_length =15)
    surname = models.TextField()
    firstname = models.TextField()
    othername = models.TextField()
    gender = models.CharField(max_length=10, choices=SEX_CHOICES, default='Male')
    programme = models.TextField()
    # passport =  models.ImageField(blank=True, default="${matric_num}.png")

    def __str__(self):
        return "%s %s %s" % (self.surname, self.firstname, self.othername)
