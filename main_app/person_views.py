import json
import math
import time
from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *

import os




def person_home(request):
    person = get_object_or_404(Person, admin=request.user)
    total_subject = Subject.objects.filter(organ=person.organ).count()
    total_attendance = AttendanceReport.objects.filter(person=person).count()
    total_present = AttendanceReport.objects.filter(person=person, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present / total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(organ=person.organ)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, person=person).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, person=person).count()
        subject_name.append(subject.name)
        data_present.append(present_count)
        data_absent.append(absent_count)
    context = {
        'total_attendance': total_attendance,
        'percent_present': percent_present,
        'percent_absent': percent_absent,
        'total_subject': total_subject,
        'subjects': subjects,
        'data_present': data_present,
        'data_absent': data_absent,
        'data_name': subject_name,
        'page_title': 'Person Homepage'

    }

    return render(request, 'person_template/home_content.html', context)


def person_view_attendance(request):
    person = get_object_or_404(Person, admin=request.user)
    if request.method != 'POST':
        organ = get_object_or_404(Organ, id=person.organ.id)
        context = {
            'subjects': Subject.objects.filter(organ=organ),
            'page_title': 'View Attendance'
        }
        return render(request, 'person_template/person_view_attendance.html', context)
    else:
        subject_id = request.POST.get('subject')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            subject = get_object_or_404(Subject, id=subject_id)
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            attendance = Attendance.objects.filter(
                date__range=(start_date, end_date), subject=subject)
            attendance_reports = AttendanceReport.objects.filter(
                attendance__in=attendance, person=person)
            json_data = []
            for report in attendance_reports:
                data = {
                    "date": str(report.attendance.date),
                    "status": report.status
                }
                json_data.append(data)
            return JsonResponse(json.dumps(json_data), safe=False)
        except Exception as e:
            return None


def person_apply_leave(request):
    form = LeaveReportPersonForm(request.POST or None)
    person = get_object_or_404(Person, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportPerson.objects.filter(person=person),
        'page_title': 'request'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.person = person
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('person_apply_leave'))
            except Exception:
                messages.error(request, "Could not submit")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "person_template/person_apply_leave.html", context)


def person_feedback(request):
    form = FeedbackPersonForm(request.POST or None)
    person = get_object_or_404(Person, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackPerson.objects.filter(person=person),
        'page_title': 'person'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.person = person
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('person_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "person_template/person_feedback.html", context)


def person_view_profile(request):
    person = get_object_or_404(Person, admin=request.user)
    form = PersonEditForm(request.POST or None, request.FILES or None,
                           instance=person)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = person.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                person.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('person_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "person_template/person_view_profile.html", context)


@csrf_exempt
def person_fcmtoken(request):
    token = request.POST.get('token')
    person_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        person_user.fcm_token = token
        person_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def person_view_notification(request):
    person = get_object_or_404(Person, admin=request.user)
    notifications = NotificationPerson.objects.filter(person=person)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "person_template/person_view_notification.html", context)


def person_view_result(request):
    person = get_object_or_404(Person, admin=request.user)
    results = PersonResult.objects.filter(person=person)
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request, "person_template/person_view_result.html", context)


def manage_person_change_password(request):
    persons = CustomUser.objects.filter(user_type=5).filter(email=request.user.email)

    context = {
        'persons': persons,
        'page_title': 'بروز رسانی پروفایل'
    }

    return render(request, "person_template/manage_person_change_password.html", context)


def edit_person_user_password(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    form = PersonFormUserEdit(request.POST or None, instance=person)
    context = {
        'form': form,
        'person_id': person_id,
        'page_title': 'Edit Person'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            organ = form.cleaned_data.get('organ')
            session = form.cleaned_data.get('session')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=person.admin.id)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                person.session = session
                user.gender = gender
                user.address = address
                person.organ = organ
                user.save()
                person.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_person_user_password', args=[person_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "person_template/edit_person_user_password_template.html", context)


def edit_person_user_picture(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    form = PersonFormUserEdit(request.POST or None, instance=person)
    context = {
        'form': form,
        'person_id': person_id,
        'page_title': 'Edit Person'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            organ = form.cleaned_data.get('organ')
            session = form.cleaned_data.get('session')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=person.admin.id)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                person.session = session
                user.gender = gender
                user.address = address
                person.organ = organ
                user.save()
                person.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_person_user_picture', args=[person_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "person_template/edit_person_user_picture_template.html", context)


def person_news(request):
    """
    persons = CustomUser.objects.filter(user_type=5).filter(email=request.user.email)

    r = requests.get('https://www.tgju.org/profile/price_dollar_rl')

    soup = BeautifulSoup(r.content, 'html.parser')

    price_tag = soup.find('td', class_='text-left')
    price1 = str(price_tag)[22:24] + ','
    price2 = str(price_tag)[24]
    price3 = str(price_tag)[26:28]
    price = price1 + price2 + price3
    prices = {'price': price}


    res = requests.get(
        'https://www.shahrekhabar.com/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%DA%AF%D9%88%D9%86%D8%A7%DA%AF%D9%88%D9%86')

    soup = bs4.BeautifulSoup(res.text, 'lxml')
    div = soup.find('a', {"class": "alink"})  # Finds the div with class "_1lwNBHmCQJObvqs1fXKSYR"
    text = div.text  # Identifies text of the div tag
    print(text)
    """

    context = {
        'persons': persons,
        'page_title': 'Manage persons'
    }

    return render(request, "person_template/person_news.html", context)

"""
def person_user_download_file(request):
    file_name = request.user.email + '.pdf'
    file_path = os.path.abspath(r"main_app/static/upload/" + file_name)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    else:
        # if this file is not found write File not found
        return render(request, 'person_template/person_user_download_file_template_not_exits.html')

    # return the main html file
    return render(request, 'person_template/person_user_download_file_template.html', context)


def person_news_1(request):
    return render(request,'person_template/person_news_1.html')
"""

def person_user_download_file(request):
    this_company = ''
    if request.user.user_type == '1':
        this_company = "admin"
    elif request.user.user_type == '2':
        this_company = "staff"
    elif request.user.user_type == '3':
        this_company = "sugar"
    elif request.user.user_type == '4':
        this_company = "kh"
    elif request.user.user_type == '20':
        this_company = "person"
    elif request.user.user_type == '5':
        this_company = "holding"
    elif request.user.user_type == '6':
        this_company = "piran"
    elif request.user.user_type == '7':
        this_company = "tomato"
    elif request.user.user_type == '8':
        this_company = "taraghi"
    elif request.user.user_type == '9':
        this_company = "tootia"
    elif request.user.user_type == '10':
        this_company = "drug"
    elif request.user.user_type == '11':
        this_company = "gen"
    elif request.user.user_type == '12':
        this_company = "iron"
    elif request.user.user_type == '13':
        this_company = "ptro"
    elif request.user.user_type == '14':
        this_company = "agriculture"
    elif request.user.user_type == '15':
        this_company = "research"

    files = []

    print(request.user.user_type)
    for filename in os.listdir("main_app/static/upload/" + this_company + '/' + request.user.email + '/'):
        file_index = {}
        file_path = 'upload/' + this_company + '/'+ request.user.email + '/' + filename
        file_index['path']=file_path
        file_index['name']=filename
        files.append(file_index)
    print('@')
    print(files)
    context = {
        'files': files,
    }
    return render(request, 'person_template/person_user_download_choice_file_template.html', context)


def person_organization_software(request):
    person = get_object_or_404(Person, admin=request.user)
    total_subject = Subject.objects.filter(organ=person.organ).count()
    total_attendance = AttendanceReport.objects.filter(person=person).count()
    total_present = AttendanceReport.objects.filter(person=person, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present / total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(organ=person.organ)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, person=person).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, person=person).count()
        subject_name.append(subject.name)
        data_present.append(present_count)
        data_absent.append(absent_count)
    context = {
        'total_attendance': total_attendance,
        'percent_present': percent_present,
        'percent_absent': percent_absent,
        'total_subject': total_subject,
        'subjects': subjects,
        'data_present': data_present,
        'data_absent': data_absent,
        'data_name': subject_name,
        'page_title': 'Person Homepage'

    }

    return render(request, 'person_template/person_organization_software.html', context)

