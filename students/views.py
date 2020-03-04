from datetime import datetime, timedelta
import time
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from students.forms import UploadStudentsForm
from django.views.generic import FormView, DetailView, ListView, View

# Create your views here.
from students.models import Student, StudentLog, Examination, Attendance


class FileFieldView(FormView):
    form_class = UploadStudentsForm
    template_name = 'students/upload.html'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        student_file = request.FILES['students_data']
        # files = request.FILES['students_images']
        if form.is_valid():
            student_file.save_book_to_database(models=[Student], initializers=[None], mapdicts=[
                {"matricnum": "matric_num", "surname": "surname", "firstname": "firstname", "othername": "othername",
                 "sex": "gender", "programme": "programme"}])
            # for f in files:
            #     print("Name of file is " + f._get_name())
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class StudentDetailView(DetailView):
    model = Student
    template_name = "students/student_details.html"

    def get_object(self, queryset=None):
        query = self.request.GET.get("matric")
        try:
            student = Student.objects.filter(matric_num=query)[0]
            studentLog = StudentLog(student=student, time=datetime.now().time(), day=datetime.now().date())
            studentLog.save()
            return student
        except Exception as e:
            print(e)
            return None


class AttendanceDetailView(DetailView):
    model = Attendance
    template_name = "students/attendance_details.html"

    def get_object(self, queryset=None):
        query = self.request.GET.get("matric")
        exam_id = self.request.GET.get("exam")
        checkout = self.request.GET.get('checkout')
        try:
            if checkout == 'true':
                student = Student.objects.get(matric_num=query)
                exam = Examination.objects.get(id=exam_id)
                attendance = Attendance.objects.get(student=student, exam=exam)
                attendance.check_out = datetime.now().time()
                attendance.save()
            else:
                student = Student.objects.get(matric_num=query)
                exam = Examination.objects.get(id=exam_id)
                attendance = Attendance(student=student, check_in=datetime.now().time(), exam=exam)
                attendance.save()
            return attendance
        except IntegrityError as e:
            student = Student.objects.get(matric_num=query)
            exam = Examination.objects.get(id=exam_id)
            return Attendance(student=student, exam=exam)
        except Exception as e:
            print(e)

            return None


class ExaminationDetailView(View):
    model = Examination

    template_name = "students/examination_details.html"

    def get(self, request, *args, **kwargs):
        examination = get_object_or_404(Examination, pk=kwargs['pk'])
        attendance = Attendance.objects.filter(exam=examination)
        valid = False
        if (examination.date == datetime.now().date() and (datetime(year= examination.date.year, month=examination.date.month, day = examination.date.day, hour=examination.start_time.hour) - timedelta(hours=1))< datetime.now() and (datetime(year= examination.date.year, month=examination.date.month, day = examination.date.day, hour=examination.start_time.hour) + timedelta(hours=1)) > datetime.now()):
            valid = True
        context = {'examination': examination, 'attendance': attendance, 'valid': valid}
        return render(request, 'students/examination_details.html', context)


class StudentsListView(ListView):
    model = Student
    paginate_by = 20
    ordering = ['surname', 'firstname', 'othername']
    template_name = "students/student_list.html"


class ExaminationListView(ListView):
    model = Examination
    paginate_by = 20
    ordering = ['-start_time', '-date']
    template_name = "students/examination_list.html"


class StudentLogListView(ListView):
    model = StudentLog
    paginate_by = 100
    ordering = ['-time', '-day']
    template_name = "students/student_log.html"
