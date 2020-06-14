from django.contrib import admin
from students.models import Student, StudentLog, Examination, Attendance, Room, Hostel, HostelAttendance, Visitor, \
    VisitingStudent, Property, SupervisorAttendance, PorterAttendance

# Register your models here.
admin.site.register(Student)
admin.site.register(StudentLog)
admin.site.register(Examination)
admin.site.register(SupervisorAttendance)
admin.site.register(PorterAttendance)
admin.site.register(Attendance)
admin.site.register(Room)
admin.site.register(Hostel)
admin.site.register(HostelAttendance)
admin.site.register(Visitor)
admin.site.register(VisitingStudent)
admin.site.register(Property)
