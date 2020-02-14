from django.urls import path
from students.views import FileFieldView, StudentDetailView
from .views import HomePageView, upload_student_records

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('dataupload/', FileFieldView.as_view(), name='dataupload'),
    path('student/', StudentDetailView.as_view(), name='student_details')
]
