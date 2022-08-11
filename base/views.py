
from math import fabs
from multiprocessing import context
import random
from time import time
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from base.forms import CourseForm, LogInForm, RatingForm, SignUpForm, VideoForm
from base.models import Cart, Course, Rating, StudentCourse, User, Video
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator


def index(request):
    latestCourses = Course.objects.all().order_by('-time')[:6]
    topRatedCourses = Course.objects.all().order_by('-rating')[:6]
    mostPopularCourses = Course.objects.all().order_by('-number_of_sold')[:6]

    context = {'login': False,
               'latestCourses': latestCourses,
               'topRatedCourses': topRatedCourses,
               'mostPopularCourses': mostPopularCourses,
               }
    user = request.user
    if user.is_authenticated:
        context = {'login': True,
                   'latestCourses': latestCourses,
                   'topRatedCourses': topRatedCourses,
                   'mostPopularCourses': mostPopularCourses,
                   'cart_count': cart_counter(request)
                   }
    return render(request, 'index.html', context)


def login(request):
    form = LogInForm()
    context = {
        'form': form,
        'error': ""
    }
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
                    context = {
                        'form': form,
                        'error': "Please Active your account first.",
                    }
                    return render(request, 'login.html', context)
            else:
                context = {
                    'form': form,
                    'error': "Invalid Username or Password.",
                }
                return render(request, 'login.html', context)
    return render(request, 'login.html', context)


def logout(request):
    auth_logout(request)
    messages.info(request, "Logout successful!")
    return redirect('/')


def signup(request):
    form = SignUpForm()
    context = {
        'form': form,
        'error': ""
    }
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            userForm = form.save(commit=False)
            domain_name = get_current_site(request).domain

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
            messages.info(
                request, f"Account Created Successful. Check Your E-mail[{email}] to verify.")
            return redirect('/login')
        else:
            form.errors
            context = {
                'form': form,
                'error': "E-mail already exists."
            }
            return render(request, 'signup.html', context)

    return render(request, 'signup.html', context)


def categories(request):
    categories = [
        {'name': 'Academics', 'imageUrl': 'Academics.png'},
        {'name': 'Business', 'imageUrl': 'Business.png'},
        {'name': 'Design', 'imageUrl': 'Design.png'},
        {'name': 'Development', 'imageUrl': 'Development.jpg'},
        {'name': 'Health & Fitness', 'imageUrl': 'Health_&_Fitness.jpeg'},
        {'name': 'IT & Software', 'imageUrl': 'IT_&_Software.jpg'},
        {'name': 'Language', 'imageUrl': 'Language.png'},
        {'name': 'Lifestyle', 'imageUrl': 'Lifestyle.png'},
        {'name': 'Marketing', 'imageUrl': 'Marketing.png'},
        {'name': 'Music', 'imageUrl': 'Music.jpg'},
        {'name': 'Office Productivity', 'imageUrl': 'Office_Productivity.jpg'},
        {'name': 'Personal Development', 'imageUrl': 'Personal_Development.jpg'},
        {'name': 'Photography', 'imageUrl': 'Photography.jpg'},
    ]
    context = {'login': False, 'categories': categories}
    user = request.user
    if user.is_authenticated:
        context = {'login': True, 'categories': categories,
                   'cart_count': cart_counter(request)}
    return render(request, 'categories.html', context)


def dashboard(request):
    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        result = []
        if user.account_type == 'Student':
            courseIds = StudentCourse.objects.filter(username=user.username)
            for id in courseIds:
                result.append(Course.objects.filter(id=id.course_id)[0])

        elif user.account_type == 'Publisher':
            result = Course.objects.filter(
                username=user.username).order_by("-time")

        context = {'login': True,
                   'user': user,
                   'courses': result,
                   'cart_count': cart_counter(request)
                   }
    return render(request, 'dashboard.html', context)


def cart(request):
    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('delete') is not None:
                data = request.POST.dict()
                id = data.get('id')
                item = Cart.objects.filter(
                    username=user.username, course_id=id)[0]
                item.delete()
                return redirect('/cart')
            elif request.POST.get('confirm_parches') is not None:
                cartItems = Cart.objects.filter(username=user.username)
                for courseId in cartItems:
                    course = Course.objects.filter(id=courseId.course_id)[0]
                    count = len(StudentCourse.objects.filter(
                        username=user.username, course_id=courseId.course_id))
                    if count == 0:
                        studentCourse = StudentCourse(
                            course_id=courseId.course_id, username=courseId.username)
                        Course.objects.filter(id=courseId.course_id).update(
                            number_of_sold=(course.number_of_sold+1))
                        studentCourse.save()
                cartItems.delete()
                return redirect('/dashboard')

        result = Cart.objects.filter(username=user.username)
        no_item = len(result) == 0
        courses = []
        totalFee = 0
        for courseId in result:
            course = Course.objects.filter(id=courseId.course_id)[0]
            totalFee += course.fee
            courses.append(course)
    context = {'login': True,
               'courses': courses,
               'total': totalFee,
               'cart_count': cart_counter(request),
               'no_item': no_item
               }
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
    result = Course.objects.filter(id=id)[0]
    reviews = Rating.objects.filter(course_id=id)
    paginator = Paginator(reviews, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user = request.user
    if request.POST.get('add_to_cart') is not None:
        if user.is_authenticated:
            count = len(Cart.objects.filter(
                username=user.username, course_id=id))
            if count == 0:
                cartItem = Cart(course_id=id, username=user.username)
                cartItem.save()
            else:
                print('already in the cart')
            return redirect('/view_course/'+id)
        else:
            return redirect('/login')
    if user.is_authenticated:
        is_soldable = len(StudentCourse.objects.filter(
            username=user.username, course_id=id)) == 0

        context = {'login': True,
                   'id': id,
                   'course': result,
                   'cart_count': cart_counter(request),
                   'is_soldable': is_soldable,
                   'page_obj': page_obj
                   }
    else:
        context = {'login': False,
                   'id': id,
                   'course': result,
                   'cart_count': cart_counter(request),
                   'is_soldable': True,
                   'page_obj': page_obj
                   }
    return render(request, 'view_course.html', context)


def add_course(request):
    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/dashboard')
        form = CourseForm()
        context = {'login': True, 'form': form,
                   'cart_count': cart_counter(request)}
    else:
        return redirect('/login')
    return render(request, 'add_course.html', context)


def edit_course(request, id):
    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                video_count = form.cleaned_data['s_id']
                form.save()
                Course.objects.filter(id=id).update(
                    video_count=video_count)
                return redirect('/edit_course/'+id)
        course = Course.objects.filter(id=int(id))[0]
        result = Video.objects.filter(course_id=int(id))
        form = VideoForm()
        context = {
            'login': True,
            'user': user,
            'course': course,
            'videos': result,
            'form': form,
            'id': id,
            'cart_count': cart_counter(request)
        }
    else:
        return redirect('/login')
    return render(request, 'edit_course.html', context)


def open_course(request, id):
    user = request.user
    if request.method == 'POST':
        form = RatingForm(request.POST, request.POST)
        if form.is_valid():
            course = Course.objects.filter(
                id=id)[0]
            current_rating = ((course.rating*course.number_of_rating) +
                              form.cleaned_data['rating'])/(course.number_of_rating+1)
            Course.objects.filter(id=id).update(
                rating=current_rating, number_of_rating=course.number_of_rating+1)
            form.save()

            return redirect('/open_course/'+id)

    course = Course.objects.filter(id=id)[0]
    videos = Video.objects.filter(course_id=id)
    is_reviewed = len(Rating.objects.filter(
        username=user.username, course_id=id)) == 0
    context = {
        'first_video': videos[0].video_file,
        'login': True,
        'is_reviewed': is_reviewed,
        'course': course,
        'videos': videos,
        'id': id,
        'cart_count': cart_counter(request)
    }
    return render(request, 'open_course.html', context)


def category(request, category):
    courses = Course.objects.filter(category=category)
    context = {
        'login': True,
        'category': category,
        'courses': courses,
        'cart_count': cart_counter(request),
    }
    return render(request, 'category.html', context)


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


def cart_counter(request):
    user = request.user
    if user.is_authenticated:
        count = len(Cart.objects.filter(username=user.username))
        # if count != 0:
        #     res = db.cart.find({'user': user.username}).next()
        #     count = len(res['courses'])
        return count
    return 0
