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

MOVING = (
    ('in', 'In'),
    ('out', 'Out'),
)


class Hostel(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Room(models.Model):
    room_number = models.TextField()
    hostel = models.ManyToManyField(to=Hostel, related_name="rooms")

    def __str__(self):
        return "%s (%s)" % (self.hostel.first().name, self.room_number)


# Create your models here.
class Student(models.Model):
    matric_num = models.CharField(max_length =15)
    surname = models.TextField()
    firstname = models.TextField()
    othername = models.TextField()
    gender = models.CharField(max_length=10, choices=SEX_CHOICES, default='Male')
    programme = models.TextField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='no')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    # passport =  models.ImageField(blank=True, default="${matric_num}.png")

    def __str__(self):
        return "%s %s %s" % (self.surname, self.firstname, self.othername)


class StudentLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    time = models.TimeField()
    day = models.DateField()

    def __str__(self):
        return "%s %s %s" % (self.student, self.day, self.time)


class Examination(models.Model):
    title = models.TextField()
    venue = models.TextField()
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


class Attendance(models.Model):
    check_in = models.TimeField()
    check_out = models.TimeField(blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['student', 'exam']

    def __str__(self):
        return  "%s %s %s" % (self.exam, self.student, self.check_in)


class HostelAttendance(models.Model):
    check_in = models.TimeField()
    check_out = models.TimeField(blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)

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
        return  self.name
