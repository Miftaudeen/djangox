from django.db import models

SEX_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
    ('Unknown', 'Unknown'),
)


PAYMENT_CHOICES = (
    ('no', 'No Payment'),
    ('partial', 'Partial Payment'),
    ('full', 'Full Payment'),
)


# Create your models here.
class Student(models.Model):
    matric_num = models.CharField(max_length =15)
    surname = models.TextField()
    firstname = models.TextField()
    othername = models.TextField()
    gender = models.CharField(max_length=10, choices=SEX_CHOICES, default='Male')
    programme = models.TextField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='no')
    # passport =  models.ImageField(blank=True, default="${matric_num}.png")

    def __str__(self):
        return "%s %s %s" % (self.surname, self.firstname, self.othername)


class StudentLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    time = models.TimeField()
    day = models.DateField()


class Examination(models.Model):
    title = models.TextField()
    venue = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.title


class Attendance(models.Model):
    check_in = models.TimeField()
    check_out = models.TimeField(blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['student', 'exam']