
from datetime import date
from email import message
import imp
from math import fabs
import os
import random
from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, hashers, logout as auth_logout
from base.forms import CourseForm, LogInForm, SignUpForm, TempForm, VideoForm
from base.models import User, Video
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
import requests
from pymongo import MongoClient
import pymongo
from django.core.files.storage import FileSystemStorage
import string
import cv2

client = MongoClient('mongodb://localhost:27017')
db = client.onlinelearning


def index(request):
    result = db.courses.find({}).sort('time', pymongo.DESCENDING).limit(3)
    context = {'login': False, 'courses': result}
    user = request.user
    if user.is_authenticated:
        context = {'login': True, 'courses': result}
    return render(request, 'index.html', context)


def login(request):
    if request.method == 'POST':
        form = LogInForm(request.POST, request.POST)
        if form.is_valid():
            email = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if(user.is_verified):
                    auth_login(request, user)
                    messages.info(request, "Login successful.")
                    return redirect('/')
                else:
                    return render(request, 'login.html', {'form': form, 'error': "Please Active your account first."})
            else:
                return render(request, 'login.html', {'form': form, 'error': "Invalid."})

    form = LogInForm()
    return render(request, 'login.html', {'form': form, 'error': ""})


def logout(request):
    auth_logout(request)
    messages.info(request, "Logout successful.")
    return redirect('/')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not User.objects.filter(email=email).exists():
                userForm = form.save(commit=False)
                domain_name = get_current_site(request).domain

                messages.info(request, "Account created successfully.")
                token = str(random.random()).split('.')[1]
                userForm.token = token
                link = f'http://{domain_name}/verify/{token}'

                send_mail(
                    'Online Learning mail verification',
                    f'Please click {link} to verify',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )

                userForm.save()

                return redirect('/login')
            else:
                messages.info(request, "E-mail already exists.")

    form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def categories(request):
    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        context = {'login': True}
    return render(request, 'categories.html', context)


def dashboard(request):
    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        result = db.courses.find({'user': user.username})
        context = {'login': True, 'user': user, 'courses': result}
    return render(request, 'dashboard.html', context)


def cart(request):
    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        context = {'login': True}
    return render(request, 'cart.html', context)


def verify(request, token):
    user = User.objects.filter(token=token)[0]

    if user.is_verified:
        messages.info(request, "Already verified.")
    else:
        user.is_verified = True
        user.save()
        messages.info(request, "Successfully Verified.")

    return redirect('/login')


def view_course(request, id):
    context = {'login': False}
    user = request.user
    if user.is_authenticated:

        result = db.courses.find({'id': id}).next()

        context = {'login': True, 'id': id, 'course': result}
    return render(request, 'view_course.html', context)


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            image = request.FILES['coverImage']
            fs = FileSystemStorage(location='media/images/')

            modified_name = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=20))
            ext = os.path.splitext(str(request.FILES['coverImage']))[1]

            fs.save(modified_name+ext, image)

            fee = 0
            course_type = form.cleaned_data['course_type']
            if course_type != 'Free':
                fee = form.cleaned_data['fee']

            course = {
                'id': modified_name,
                'category': form.cleaned_data['category'],
                'imageUrl': modified_name+ext,
                'user': request.user.username,
                'title': form.cleaned_data['title'],
                'outcome': form.cleaned_data['outcome'],
                'requirement': form.cleaned_data['requirement'],
                'description': form.cleaned_data['description'],
                'rating': 0,
                'numberOfRating': 0,
                'uploadDate': f'{date.today():%b %d, %Y}',
                'time': datetime.utcnow(),
                'course_type': course_type,
                'fee': fee,
                'videoCount': 0,
                'videos': {}
            }
            db.courses.insert(course)
            return redirect('/dashboard')
    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        form = CourseForm()
        context = {'login': True, 'form': form}
    else:
        return redirect('/login')
    return render(request, 'add_course.html', context)


def edit_course(request, id):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = request.FILES['video_file']
            fs = FileSystemStorage(location='media/videos/')

            modified_name = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=20))
            ext = os.path.splitext(str(request.FILES['video_file']))[1]

            fs.save(modified_name+ext, video)

            video = cv2.VideoCapture("media/videos/"+modified_name+ext)

            frame_rate = video.get(cv2.CAP_PROP_FPS)

            total_num_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

            duration = total_num_frames / frame_rate

            result = db.courses.find({'id': id}).next()
            count = result['videoCount']
            count += 1
            videoFile = {f'{count}': {
                'id': modified_name,
                's_id': count,
                'extension': ext,
                'title': form.cleaned_data['title'],
                'duration': time_format(duration)
            }}

            result = db.courses.find({'id': id}).next()

            rj = result['videos']
            rj.update(videoFile)

            filter = {'id': id}
            nol = {'$set': {'videos': rj, 'videoCount': count}}
            db.courses.update_one(filter, nol)

    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        result = db.courses.find({'id': id}).next()
        form = VideoForm()
        context = {
            'login': True,
            'user': user,
            'course': result,
            'form': form,
            'id': id
        }
    else:
        return redirect('/login')
    return render(request, 'edit_course.html', context)


def time_format(seconds: int):
    if seconds is not None:
        seconds = int(seconds)
        h = seconds // 3600 % 24
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        if h > 0:
            return '{:02d}:{:02d}:{:02d}s'.format(h, m, s)
        else:
            return '{:02d}:{:02d}'.format(m, s)
