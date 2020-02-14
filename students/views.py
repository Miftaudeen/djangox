from django.shortcuts import render
from django.urls import reverse_lazy
import django_excel
from students.forms import UploadStudentsForm
from django.views.generic import FormView, DetailView

# Create your views here.
from students.models import Student


class FileFieldView(FormView):
    form_class = UploadStudentsForm
    template_name = 'students/upload.html'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        student_file = request.FILES['students_data']
        files = request.FILES['students_images']
        if form.is_valid():
            student_file.save_book_to_database(models=[Student], initializers=[None], mapdicts=[{"matricnum":"matric_num", "surname": "surname", "firstname": "firstname", "othername": "othername", "sex": "gender", "programme": "programme"}])
            for f in files:
                print("Name of file is " + f._get_name())
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class StudentDetailView(DetailView):
    model = Student
    template_name = "students/student_details.html"

    def get_object(self, queryset=None):
        query = self.request.GET.get("matric")
        return Student.objects.filter(matric_num=query)[0]