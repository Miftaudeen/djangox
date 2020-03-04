from django.contrib import admin
from students.models import Student, StudentLog, Examination, Attendance

# Register your models here.
admin.site.register(Student)
admin.site.register(StudentLog)
admin.site.register(Examination)
admin.site.register(Attendance)
