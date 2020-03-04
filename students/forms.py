from django import forms
class UploadStudentsForm(forms.Form):
    students_data = forms.FileField()
    # students_images = forms.FileField(widget=forms.ClearableFileInput(attrs=
    #     {'multiple': True, 'webkitdirectory': True, 'directory': True}))