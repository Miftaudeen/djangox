from datetime import datetime, timedelta
import time

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from students.forms import UploadStudentsForm
from django.views.generic import FormView, DetailView, ListView, View

# Create your views here.
from students.models import Student, StudentLog, Examination, Attendance, Hostel, HostelAttendance, Room, Visitor, \
    VisitingStudent, Property


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


class VisitorDetailView(DetailView):
    model = Visitor
    template_name = "students/visitor_details.html"

    def get_object(self, queryset=None):
        query = self.request.GET.get("visitor")
        student_id = self.request.GET.get("student")
        name = self.request.GET.get("name")
        phone_number = self.request.GET.get("phone_number")
        address = self.request.GET.get("address")
        checkout = self.request.GET.get('checkout')
        try:
            if checkout == 'true':
                visitor = Visitor.objects.get(id=query)
                visitor.departure_time = datetime.now()
                visitor.save()
            else:
                student = Student.objects.get(id=student_id)
                visitor = Visitor(student=student, arrival_time=datetime.now(), name=name, phone_number=phone_number, address=address)
                visitor.save()
            return visitor
        except Exception as e:
            print(e)

            return None


class StudentVisitorDetailView(DetailView):
    model = VisitingStudent
    template_name = "students/student_visitor_details.html"

    def get_object(self, queryset=None):
        query = self.request.GET.get("matric")
        visitor_id = self.request.GET.get("visitor")
        host = self.request.GET.get("host")
        checkout = self.request.GET.get('checkout')
        try:
            if checkout == 'true':
                visitor = VisitingStudent.objects.get(id=visitor_id)
                visitor.departure_time = datetime.now()
                visitor.save()
                return visitor
            else:
                student = Student.objects.get(id=host)
                visitor = Student.objects.get(matric_num=query)
                student_visitor = VisitingStudent(student=student, visitor=visitor, arrival_time= datetime.now())
                student_visitor.save()
            return student_visitor
        except Exception as e:
            print(e)

            return None



class StudentPropertyDetailView(DetailView):
    model = Property
    template_name = "students/student_property_details.html"

    def get_object(self, queryset=None):
        student_id = self.request.GET.get("student")
        name = self.request.GET.get("name")
        mover = self.request.GET.get("mover")
        description = self.request.GET.get("description")
        moving = self.request.GET.get("moving")
        try:
            student = Student.objects.get(id=student_id)
            student_property = Property(student=student, name=name, mover=mover, description=description, moving=moving,
                                        timestamp=datetime.now())
            student_property.save()
            return student_property
        except Exception as e:
            print(e)
            return None


class HostelAttendanceDetailView(DetailView):
    model = HostelAttendance
    template_name = "students/hostel_attendance_details.html"

    def get_object(self, queryset=None):
        query = self.request.GET.get("matric")
        hostel_id = self.request.GET.get("hostel")
        checkout = self.request.GET.get('checkout')
        try:
            if checkout == 'true':
                student = Student.objects.get(matric_num=query)
                hostel = Hostel.objects.get(id=hostel_id)
                attendance = HostelAttendance.objects.get(student=student, hostel=hostel)
                attendance.check_out = datetime.now().time()
                attendance.save()
            else:
                student = Student.objects.get(matric_num=query)
                hostel = Hostel.objects.get(id=hostel_id)
                attendance = HostelAttendance(student=student, check_in=datetime.now().time(), hostel=hostel)
                attendance.save()
            return attendance
        except IntegrityError as e:
            student = Student.objects.get(matric_num=query)
            hostel = Hostel.objects.get(id=hostel_id)
            return HostelAttendance(student=student, hostel=hostel)
        except Exception as e:
            print(e)

            return None


class HostelDetailView(View):
    model = Hostel
    template_name = "students/hostel_details.html"

    def get(self, request, *args, **kwargs):
        hostel = get_object_or_404(Hostel, pk=kwargs['pk'])
        hostel_attendance = HostelAttendance.objects.filter(hostel=hostel)
        rooms = Room.objects.filter(hostel=hostel)
        students = []
        for room in rooms:
            for student in room.students.iterator():
                students.append(student)
        context = {'hostel': hostel, 'hostel_attendance': hostel_attendance, 'rooms': rooms, 'students': students}
        return render(request, 'students/hostel_details.html', context)


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


class HostelStudentDetailView(View):
    model = Student
    template_name = "students/hostel_student_details.html"

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs['pk'])
        visitors = Visitor.objects.filter(student=student)
        student_visitors = VisitingStudent.objects.filter(student=student)
        properties = Property.objects.filter(student=student)
        context = {'student': student, 'visitors': visitors, 'student_visitors': student_visitors, 'properties': properties}
        return render(request, 'students/hostel_student_details.html', context)


class StudentsListView(ListView):
    model = Student
    paginate_by = 20
    ordering = ['surname', 'firstname', 'othername']
    template_name = "students/student_list.html"


class HostelResidentsView(ListView):
    model = Student
    paginate_by = 20
    ordering = ['surname', 'firstname', 'othername']
    template_name = "students/hostel_residents_list.html"

    def get_context_data(self, **kwargs):
        context = super(HostelResidentsView, self).get_context_data(**kwargs)
        hostel = get_object_or_404(Hostel, pk=self.request.GET['pk'])
        students = Student.objects.filter(room__hostel=hostel)
        paginator = Paginator(students, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)
        context["hostel"] = hostel
        context['students'] = students
        return context


class ExaminationListView(ListView):
    model = Examination
    paginate_by = 20
    ordering = ['-start_time', '-date']
    template_name = "students/examination_list.html"


class HostelListView(ListView):
    model = Hostel
    paginate_by = 20
    ordering = ['name']
    template_name = "students/hostel_list.html"


class StudentLogListView(ListView):
    model = StudentLog
    paginate_by = 100
    ordering = ['-time', '-day']
    template_name = "students/student_log.html"
