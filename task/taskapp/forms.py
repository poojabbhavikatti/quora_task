from django import forms
from django.contrib.auth.models import User
from taskapp.models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

class user_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','email','password')                                #'__all__'

# class user_profileform(forms.ModelForm):
#     class Meta:
#         model = userprofile
#         fields = ('user_img','user_url')
