from django.urls import path
from students.views import FileFieldView, StudentDetailView, StudentsListView, StudentLogListView, ExaminationListView, \
    ExaminationDetailView, AttendanceDetailView, HostelListView, HostelDetailView, HostelAttendanceDetailView, \
    HostelStudentDetailView, VisitorDetailView, StudentVisitorDetailView, StudentPropertyDetailView, approve_attendance, \
    approve_hostel_attendance, HostelPorterAttendanceDetailView, ExaminationSupervisorDetailView, \
    ManagementReportListView
from .views import HomePageView, upload_student_records




urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('dataupload/', FileFieldView.as_view(), name='dataupload'),
    path('student/', StudentDetailView.as_view(), name='student_details'),
    path('attendance/', AttendanceDetailView.as_view(), name='attendance_details'),
    path('student/visitor', VisitorDetailView.as_view(), name='visitor_details'),
    path('student/property', StudentPropertyDetailView.as_view(), name='student_property_details'),
    path('student/studentvisitor', StudentVisitorDetailView.as_view(), name='student_visitor_attendance'),
    path('hostel/attendance/', HostelAttendanceDetailView.as_view(), name='hostel_attendance_details'),
    path('hostel/porter/attendance/', HostelPorterAttendanceDetailView.as_view(), name='hostel_porter_attendance'),
    path('examination/<int:pk>/', ExaminationDetailView.as_view(), name='examination_details'),
    path('examination/<int:pk>/report/', ExaminationSupervisorDetailView.as_view(), name='supervisor_report'),
    path('hostel/student/<int:pk>/', HostelStudentDetailView.as_view(), name='hostel_student_details'),
    path('hostel/<int:pk>/', HostelDetailView.as_view(), name='hostel_details'),
    path('students/', StudentsListView.as_view(), name='student_list'),
    path('management/report', ManagementReportListView.as_view(), name='management_report'),
    path('examinations/', ExaminationListView.as_view(), name='examination_list'),
    path('examinations/approve', approve_attendance, name='approve_attendance'),
    path('hostel/approve', approve_hostel_attendance, name='approve_hostel_attendance'),
    path('hostels/', HostelListView.as_view(), name='hostel_list'),
    path('studentslog/', StudentLogListView.as_view(), name='student_log'),
]
