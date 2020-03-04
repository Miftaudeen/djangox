from django.views.generic import TemplateView
from students.forms import UploadStudentsForm
from django.shortcuts import render


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


def upload_student_records(request):
    if request.method == 'POST':
        form = UploadStudentsForm(request.POST, request.FILES)
        if form.is_valid():
            student_data = request.FILES['student_data']
            student_passport = request.FILES['student_images']
            print(student_data)
            print(student_passport)
            render(request, 'pages/about.html')
    else:
        form = UploadStudentsForm()
    return render(request, 'students/upload.html', {'form': form, 'title':'Upload Student Data'})
