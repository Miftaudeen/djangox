from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse

from users.models import CustomUser

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

MOVING = (
    ('in', 'In'),
    ('out', 'Out'),
)


class Hostel(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


# Create your models here.
class Student(models.Model):
    matric_num = models.CharField(max_length =15)
    surname = models.TextField()
    firstname = models.TextField()
    othername = models.TextField()
    gender = models.CharField(max_length=10, choices=SEX_CHOICES, default='Male')
    programme = models.TextField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='no')
    hostel_name = models.ForeignKey('Hostel', on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True, related_name="residents")
    # passport =  models.ImageField(blank=True, default="${matric_num}.png")

    def __str__(self):
        return "%s %s %s" % (self.surname, self.firstname, self.othername)


class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=5, default="%s %s" % (hostel, id))
    floor = models.CharField(max_length=1, blank=True)
    wing = models.CharField(max_length=1, blank=True)
    comment = models.CharField(max_length=100, blank=True, default="comment here")
    room_capacity = models.PositiveSmallIntegerField(validators=[MaxValueValidator(8), ], default=3)
    room_accommodation = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('room-detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Room Record"


class StudentLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    time = models.TimeField()
    day = models.DateField()

    def __str__(self):
        return "%s %s %s" % (self.student, self.day, self.time)


class Examination(models.Model):
    title = models.TextField()
    venue = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


class Attendance(models.Model):
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name="exam_attendance")
    remark = models.TextField(null=True, blank=True)
    valid = models.BooleanField(default=False)

    class Meta:
        unique_together = ['student', 'exam']

    def __str__(self):
        return "%s %s %s" % (self.exam, self.student, self.check_in)


class HostelAttendance(models.Model):
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="hostel_attendance")
    valid = models.BooleanField(default=False)
    remark = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s %s %s" % (self.hostel, self.student, self.check_in)


class Visitor(models.Model):
    name = models.TextField()
    phone_number = models.TextField()
    address = models.TextField(null=True, blank=True)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField(null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='visitors')

    def __str__(self):
        return self.name


class VisitingStudent(models.Model):
    visitor = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='visits',)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField(null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_visitors')

    def __str__(self):
        return "%s %s %s" % (self.visitor.surname, self.visitor.firstname, self.visitor.othername)


class Property(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_properties')
    name = models.TextField()
    description = models.TextField()
    moving = models.CharField(max_length=3, choices=MOVING)
    mover = models.TextField()
    timestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.name


class PorterAttendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='porter_attendances')
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField(null=True, blank=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='hostel_porter_attendance')

    def __str__(self):
        return self.user.staff_id_number


class SupervisorAttendance(models.Model):
    supervisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='supervisor_attendances')
    submission_time = models.DateTimeField()
    other_supervisor = models.TextField()
    remark = models.CharField(max_length=5000)
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name='examination_supervisors')

    def __str__(self):
        return "%s %s" % (self.supervisor.last_name, self.supervisor.first_name)
