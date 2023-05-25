from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, AnswerForm, user_form
from .models import Question, Answer, Like
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

# Create your views here.
# def base(request):
#     return render(request,'base.html')

# def home(request):
#     return render(request,'home.html')

def index(request):
    return render(request,'index.html')


def home(request):
    questions = Question.objects.all()
    return render(request, 'home.html', {'questions': questions})


def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('taskapp:home')
    else:
        form = QuestionForm()
    return render(request, 'ask_questions.html', {'form': form})


def answer_question(request, question_id):
    question = Question.objects.get(id=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('answer_question', question_id=question.id)
    else:
        form = AnswerForm()
    return render(request, 'answer_question.html', {'form': form, 'question': question})


def like_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    like, created = Like.objects.get_or_create(user=request.user, answer=answer)

    if not created:
        like.delete()

    return redirect('answer_question', question_id=answer.question.id)

def register(request):
    register = False
    if request.method =='POST':
        userform = user_form(request.POST)

        if userform.is_valid():
           user = userform.save()
           user.set_password(user.password)
           user.save()

           register = True
    else:
        userform = user_form()
    return render(request,'registration.html',{'userform':userform,'register':register})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('taskapp:home'))
            else:
                return HttpResponse("<h1>User is not active</h1> ")
        else:
            return HttpResponse("<h1>Invalid creds</h1>")
    return render(request,'login.html')

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         user = authenticate(request,username=username,password=password)
#         if user:
#             # if user.is_active:
#             login(request,user)
#             return redirect(request.GET.get('next', '/'))
#                 # return HttpResponseRedirect(reverse('taskapp:base'))
#         else:
#             error_message = 'Invalid username or password.'
#             return render(request, 'login.html', {'error_message': error_message})
#                 # return HttpResponse("<h1>User is not active</h1> ")
#     else:
#         return render(request, 'login.html')
#             # return HttpResponse("<h1>Invalid credentials</h1>")
#     # return render(request,'login.html')
# @login_required


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('taskapp:home'))