from datetime import datetime, timedelta
import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic.list import MultipleObjectMixin

from students.forms import UploadStudentsForm
from django.views.generic import FormView, DetailView, ListView, View

# Create your views here.
from students.models import Student, StudentLog, Examination, Attendance, Hostel, HostelAttendance, Room, Visitor, \
    VisitingStudent, Property, PorterAttendance, SupervisorAttendance
from users.models import CustomUser


class FileFieldView(LoginRequiredMixin, FormView):

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


class StudentDetailView(LoginRequiredMixin, DetailView):
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


class AttendanceDetailView(LoginRequiredMixin,  DetailView):
    model = Attendance
    template_name = "students/attendance_details.html"

    def get_object(self, queryset=None):
        query = self.request.GET.get("matric")
        exam_id = self.request.GET.get("exam")
        checkout = self.request.GET.get('checkout')
        remark = self.request.GET.get('remark')
        try:
            if checkout == 'true':
                student = Student.objects.get(matric_num=query)
                exam = Examination.objects.get(id=exam_id)
                attendance = Attendance.objects.get(student=student, exam=exam)
                attendance.check_out = datetime.now()
                attendance.remark = remark
                attendance.save()
            else:
                student = Student.objects.get(matric_num=query)
                exam = Examination.objects.get(id=exam_id)
                attendance = Attendance(student=student, check_in=datetime.now(), exam=exam)
                attendance.save()
            return attendance
        except IntegrityError as e:
            student = Student.objects.get(matric_num=query)
            exam = Examination.objects.get(id=exam_id)
            return Attendance(student=student, exam=exam)
        except Exception as e:
            print(e)

            return None


class VisitorDetailView(LoginRequiredMixin, DetailView):
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


class StudentVisitorDetailView(LoginRequiredMixin, DetailView):
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


class StudentPropertyDetailView(LoginRequiredMixin, DetailView):
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
        attend_id = self.request.GET.get("attend_id")
        checkout = self.request.GET.get('checkout')
        try:
            if checkout == 'true':
                attendance = HostelAttendance.objects.get(id=attend_id)
                attendance.check_out = datetime.now()
                attendance.save()
            else:
                student = Student.objects.get(matric_num=query)
                hostel = Hostel.objects.get(id=hostel_id)
                attendance = HostelAttendance(student=student, check_in=datetime.now(), hostel=hostel)
                attendance.save()
            return attendance
        except IntegrityError as e:
            student = Student.objects.get(matric_num=query)
            hostel = Hostel.objects.get(id=hostel_id)
            return HostelAttendance(student=student, hostel=hostel)
        except Exception as e:
            print(e)

            return None


class HostelPorterAttendanceDetailView(DetailView):
    model = PorterAttendance
    template_name = "students/hostel_porter_attendance_details.html"

    def get_object(self, queryset=None):
        p_a_id = self.request.GET.get("p_a_id")
        p_s_id = self.request.GET.get("p_s_id")
        hostel_id = self.request.GET.get("hostel")
        depart_time = self.request.GET.get('depart_time')
        try:
            if depart_time == 'true':
                attendance = PorterAttendance.objects.get(id=p_a_id)
                attendance.departure_time = datetime.now()
                attendance.save()
            else:
                hostel = Hostel.objects.get(id=hostel_id)
                staff = CustomUser.objects.get(id=p_s_id, role="Porter")
                if staff:
                    attendance = PorterAttendance(user=self.request.user, check_in=datetime.now(), hostel=hostel)
                    attendance.save()
                else:
                    attendance = PorterAttendance()
            return attendance
        except Exception as e:
            print(e)

            return PorterAttendance()


class ExaminationSupervisorDetailView(DetailView):
    model = SupervisorAttendance
    template_name = "students/examination_supervisor_attendance_details.html"

    def get_object(self, queryset=None):
        exam_id = self.request.GET.get("exam")
        other_supervisors = self.request.GET.get("others")
        report = self.request.GET.get("report")
        try:
            exam = Examination.objects.get(id=exam_id)
            staff = CustomUser.objects.get(id=self.request.user.id, role="Supervisor")
            if staff:
                attendance = SupervisorAttendance(supervisor=staff, other_supervisor=other_supervisors,
                                                  submission_time=timezone.now(), examination=exam, remark=report)
                attendance.save()
            else:
                attendance = SupervisorAttendance()
            return attendance
        except Exception as e:
            print(e)

            return SupervisorAttendance()


class HostelDetailView(LoginRequiredMixin, View):
    model = Hostel
    template_name = "students/hostel_details.html"

    def get(self, request, *args, **kwargs):
        hostel = get_object_or_404(Hostel, pk=kwargs['pk'])
        valid_hostel_attendance = HostelAttendance.objects.filter(hostel=hostel, valid=True)
        invalid_hostel_attendance = HostelAttendance.objects.filter(hostel=hostel, valid=False)
        rooms = Room.objects.filter(hostel=hostel)
        porter_attendance = PorterAttendance.objects.filter(departure_time=None, hostel=hostel)
        if porter_attendance.all().count() == 0:
            pt = PorterAttendance(arrival_time=datetime.now(), user=request.user, hostel=hostel)
            pt.save()
            porter_attendance = PorterAttendance.objects.filter(departure_time=None, hostel=hostel)
        students = []
        for room in rooms:
            for student in room.students.iterator():
                students.append(student)
        context = {'hostel': hostel,
                   'valid_hostel_attendance': valid_hostel_attendance,
                   'invalid_hostel_attendance': invalid_hostel_attendance,
                   'rooms': rooms,
                   'porter_attendance': porter_attendance,
                   'students': students}
        return render(request, 'students/hostel_details.html', context)


class ExaminationDetailView(LoginRequiredMixin, View):
    model = Examination

    template_name = "students/examination_details.html"

    def get(self, request, *args, **kwargs):
        examination = get_object_or_404(Examination, pk=kwargs['pk'])
        valid_attendance = Attendance.objects.filter(exam=examination, valid=True)
        invalid_attendance = Attendance.objects.filter(exam=examination, valid=False)
        super_attend = SupervisorAttendance.objects.filter(examination=examination, supervisor=self.request.user)
        try:
            super_report = SupervisorAttendance.objects.get(examination=examination)
        except Exception:
            super_report = None
        valid = False
        if examination.end_time > datetime.now(tz=timezone.get_current_timezone()):
            valid = True
        context = {'examination': examination,
                   'valid_attendance': valid_attendance,
                   'invalid_attendance': invalid_attendance,
                   'valid': valid,
                   'super_attend': super_attend,
                   'super_report': super_report,
                   }
        return render(request, 'students/examination_details.html', context)


class HostelStudentDetailView(LoginRequiredMixin, View):
    model = Student
    template_name = "students/hostel_student_details.html"

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs['pk'])
        visitors = Visitor.objects.filter(student=student)
        student_visitors = VisitingStudent.objects.filter(student=student)
        properties = Property.objects.filter(student=student)
        context = {'student': student, 'visitors': visitors, 'student_visitors': student_visitors, 'properties': properties}
        return render(request, 'students/hostel_student_details.html', context)


class StudentsListView(LoginRequiredMixin, ListView):
    model = Student
    paginate_by = 20
    ordering = ['surname', 'firstname', 'othername']
    template_name = "students/student_list.html"


class HostelResidentsView(LoginRequiredMixin, ListView):
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


class ExaminationListView(LoginRequiredMixin, ListView):
    model = Examination
    paginate_by = 20
    ordering = ['-start_time']
    template_name = "students/examination_list.html"


class HostelListView(LoginRequiredMixin, ListView):
    model = Hostel
    paginate_by = 20
    ordering = ['name']
    template_name = "students/hostel_list.html"


class ManagementReportListView(LoginRequiredMixin, ListView):
    model = Examination
    paginate_by = 20
    ordering = ['start_time']
    template_name = "students/management_report_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hostels'] = Hostel.objects.all()
        context['supervisors_attendance'] = SupervisorAttendance.objects.all()
        return context


class StudentLogListView(LoginRequiredMixin, ListView):
    model = StudentLog
    paginate_by = 100
    ordering = ['-day', '-time']
    template_name = "students/student_log.html"


@login_required
def approve_attendance(request):
    is_valid = request.GET.get("valid")
    attendance = Attendance.objects.get(id=request.GET.get("attendance_id"))
    exam_id = request.GET.get("examination_id")
    reason = request.GET.get("reason")
    attendance.remark = reason
    attendance.valid = True if is_valid else False
    attendance.save()
    return HttpResponseRedirect(reverse("examination_details", args=[exam_id]))


@login_required
def approve_hostel_attendance(request):
    is_valid = request.GET.get("valid")
    hostelattendance = HostelAttendance.objects.get(id=request.GET.get("hostelattendance_id"))
    hostel_id = request.GET.get("hostel_id")
    reason = request.GET.get("reason")
    hostelattendance.remark = reason
    hostelattendance.valid = True if is_valid else False
    hostelattendance.save()
    return HttpResponseRedirect(reverse("hostel_details", args=[hostel_id]))

