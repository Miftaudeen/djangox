from django.urls import path
from students.views import FileFieldView, StudentDetailView, StudentsListView, StudentLogListView, ExaminationListView, \
    ExaminationDetailView, AttendanceDetailView
from .views import HomePageView, upload_student_records

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('dataupload/', FileFieldView.as_view(), name='dataupload'),
    path('student/', StudentDetailView.as_view(), name='student_details'),
    path('attendance/', AttendanceDetailView.as_view(), name='attendance_details'),
    path('examination/<int:pk>/', ExaminationDetailView.as_view(), name='examination_details'),
    path('students/', StudentsListView.as_view(), name='student_list'),
    path('examinations/', ExaminationListView.as_view(), name='examination_list'),
    path('studentslog/', StudentLogListView.as_view(), name='student_log'),
]
