from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken.views import  obtain_auth_token
from django.contrib.staticfiles.urls import static

# Serializers define the API representation.
from rest_framework import serializers, viewsets, routers

from students.models import Student, Room, Hostel, Examination, Attendance, SupervisorAttendance, PorterAttendance, \
    Property, Visitor, StudentLog, HostelAttendance, VisitingStudent
from users.models import CustomUser, CustomAuthToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    hostel = serializers.StringRelatedField(many=True)
    class Meta:
        model = Room
        fields = ["room_number", "hostel"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"


class ExaminationSerializer(serializers.ModelSerializer):
    exam_attendance = AttendanceSerializer(many=True,)
    class Meta:
        model = Examination
        fields = ["id", "title", "venue", "start_time", "end_time", "exam_attendance"]


class SupervisorAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorAttendance
        fields = "__all__"


class PorterAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PorterAttendance
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"


class StudentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLog
        fields = "__all__"


class HostelAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelAttendance
        fields = "__all__"


class HostelSerializer(serializers.ModelSerializer):
    hostel_attendance = HostelAttendanceSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    residents= StudentSerializer(many=True,)
    class Meta:
        model = Hostel
        fields = ["id", "name", "rooms", "hostel_attendance", "residents"]


class VisitingStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitingStudent
        fields = "__all__"


# ViewSets define the view behavior.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# ViewSets define the view behavior.
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


# ViewSets define the view behavior.
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


# ViewSets define the view behavior.
class SupervisorAttendanceViewSet(viewsets.ModelViewSet):
    queryset = SupervisorAttendance.objects.all()
    serializer_class = SupervisorAttendanceSerializer


# ViewSets define the view behavior.
class PorterAttendanceViewSet(viewsets.ModelViewSet):
    queryset = PorterAttendance.objects.all()
    serializer_class = PorterAttendanceSerializer


# ViewSets define the view behavior.
class HostelViewSet(viewsets.ModelViewSet):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer


# ViewSets define the view behavior.
class HostelAttendanceViewSet(viewsets.ModelViewSet):
    queryset = HostelAttendance.objects.all()
    serializer_class = HostelAttendanceSerializer


# ViewSets define the view behavior.
class VisitingStudentViewSet(viewsets.ModelViewSet):
    queryset = VisitingStudent.objects.all()
    serializer_class = VisitingStudentSerializer


# ViewSets define the view behavior.
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


# ViewSets define the view behavior.
class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer


# ViewSets define the view behavior.
class ExaminationViewSet(viewsets.ModelViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer


# ViewSets define the view behavior.
class StudentLogViewSet(viewsets.ModelViewSet):
    queryset = StudentLog.objects.all()
    serializer_class = StudentLogSerializer


# ViewSets define the view behavior.
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'hostels', HostelViewSet)
router.register(r'hostel_attendances', HostelAttendanceViewSet)
router.register(r'visiting_students', VisitingStudentViewSet)
router.register(r'porter_attendances', PorterAttendanceViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'visitors', VisitorViewSet)
router.register(r'examinations', ExaminationViewSet)
router.register(r'supervisor_attendances', SupervisorAttendanceViewSet)
router.register(r'student_logs', StudentLogViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    re_path(r'^api-token-auth/', CustomAuthToken.as_view()),
    path('accounts/', include('allauth.urls')),
    path('api/', include(router.urls)),
    path('', include('pages.urls')),
    re_path(r'^api-auth/', include('rest_framework.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
