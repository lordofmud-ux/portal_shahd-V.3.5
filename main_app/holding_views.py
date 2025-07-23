
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




def holding_home(request):
    holding = get_object_or_404(Holding, admin=request.user)
    total_subject = Subject.objects.filter(organ=holding.organ).count()
    total_attendance = AttendanceReport.objects.filter(holding=holding).count()
    total_present = AttendanceReport.objects.filter(holding=holding, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present / total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(organ=holding.organ)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, holding=holding).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, holding=holding).count()
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
        'page_title': 'Holding Homepage'

    }

    return render(request, 'holding_template/home_content.html', context)


def holding_view_attendance(request):
    holding = get_object_or_404(Holding, admin=request.user)
    if request.method != 'POST':
        organ = get_object_or_404(Organ, id=holding.organ.id)
        context = {
            'subjects': Subject.objects.filter(organ=organ),
            'page_title': 'View Attendance'
        }
        return render(request, 'holding_template/holding_view_attendance.html', context)
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
                attendance__in=attendance, holding=holding)
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


def holding_apply_leave(request):
    form = LeaveReportHoldingForm(request.POST or None)
    holding = get_object_or_404(Holding, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportHolding.objects.filter(holding=holding),
        'page_title': 'request'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.holding = holding
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('holding_apply_leave'))
            except Exception:
                messages.error(request, "Could not submit")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "holding_template/holding_apply_leave.html", context)


def holding_feedback(request):
    form = FeedbackHoldingForm(request.POST or None)
    holding = get_object_or_404(Holding, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackHolding.objects.filter(holding=holding),
        'page_title': 'holding'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.holding = holding
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('holding_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "holding_template/holding_feedback.html", context)


def holding_view_profile(request):
    holding = get_object_or_404(Holding, admin=request.user)
    form = HoldingEditForm(request.POST or None, request.FILES or None,
                           instance=holding)
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
                admin = holding.admin
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
                holding.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('holding_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "holding_template/holding_view_profile.html", context)


@csrf_exempt
def holding_fcmtoken(request):
    token = request.POST.get('token')
    holding_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        holding_user.fcm_token = token
        holding_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def holding_view_notification(request):
    holding = get_object_or_404(Holding, admin=request.user)
    notifications = NotificationHolding.objects.filter(holding=holding)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "holding_template/holding_view_notification.html", context)


def holding_view_result(request):
    holding = get_object_or_404(Holding, admin=request.user)
    results = HoldingResult.objects.filter(holding=holding)
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request, "holding_template/holding_view_result.html", context)


def manage_holding_change_password(request):
    holdings = CustomUser.objects.filter(user_type=5).filter(email=request.user.email)

    context = {
        'holdings': holdings,
        'page_title': 'بروز رسانی پروفایل'
    }

    return render(request, "holding_template/manage_holding_change_password.html", context)


def edit_holding_user_password(request, holding_id):
    holding = get_object_or_404(Holding, id=holding_id)
    form = HoldingFormUserEdit(request.POST or None, instance=holding)
    context = {
        'form': form,
        'holding_id': holding_id,
        'page_title': 'Edit Holding'
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
                user = CustomUser.objects.get(id=holding.admin.id)
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
                holding.session = session
                user.gender = gender
                user.address = address
                holding.organ = organ
                user.save()
                holding.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_holding_user_password', args=[holding_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "holding_template/edit_holding_user_password_template.html", context)


def edit_holding_user_picture(request, holding_id):
    holding = get_object_or_404(Holding, id=holding_id)
    form = HoldingFormUserEdit(request.POST or None, instance=holding)
    context = {
        'form': form,
        'holding_id': holding_id,
        'page_title': 'Edit Holding'
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
                user = CustomUser.objects.get(id=holding.admin.id)
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
                holding.session = session
                user.gender = gender
                user.address = address
                holding.organ = organ
                user.save()
                holding.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_holding_user_picture', args=[holding_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "holding_template/edit_holding_user_picture_template.html", context)


def holding_news(request):
    holdings = CustomUser.objects.filter(user_type=5).filter(email=request.user.email)

    r = requests.get('https://www.tgju.org/profile/price_dollar_rl')

    soup = BeautifulSoup(r.content, 'html.parser')

    price_tag = soup.find('td', class_='text-left')
    price1 = str(price_tag)[22:24] + ','
    price2 = str(price_tag)[24]
    price3 = str(price_tag)[26:28]
    price = price1 + price2 + price3
    prices = {'price': price}

    '''
    res = requests.get(
        'https://www.shahrekhabar.com/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%DA%AF%D9%88%D9%86%D8%A7%DA%AF%D9%88%D9%86')

    soup = bs4.BeautifulSoup(res.text, 'lxml')
    div = soup.find('a', {"class": "alink"})  # Finds the div with class "_1lwNBHmCQJObvqs1fXKSYR"
    text = div.text  # Identifies text of the div tag
    print(text)
    '''

    context = {
        'prices': prices,
        'holdings': holdings,
        'page_title': 'Manage holdings'
    }

    return render(request, "holding_template/holding_news.html", context)

"""
def holding_user_download_file(request):
    file_name = request.user.email + '.pdf'
    file_path = os.path.abspath(r"main_app/static/upload/" + file_name)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    else:
        # if this file is not found write File not found
        return render(request, 'holding_template/holding_user_download_file_template_not_exits.html')

    # return the main html file
    return render(request, 'holding_template/holding_user_download_file_template.html', context)


def holding_news_1(request):
    return render(request,'holding_template/holding_news_1.html')
"""

def holding_user_download_file(request):
    this_company = ''
    if request.user.user_type == '1':
        this_company = "admin"
    elif request.user.user_type == '2':
        this_company = "staff"
    elif request.user.user_type == '3':
        this_company = "sugar"
    elif request.user.user_type == '4':
        this_company = "kh"
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
    return render(request, 'holding_template/holding_user_download_choice_file_template.html', context)


def holding_organization_software(request):
    holding = get_object_or_404(Holding, admin=request.user)
    total_subject = Subject.objects.filter(organ=holding.organ).count()
    total_attendance = AttendanceReport.objects.filter(holding=holding).count()
    total_present = AttendanceReport.objects.filter(holding=holding, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present / total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(organ=holding.organ)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, holding=holding).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, holding=holding).count()
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
        'page_title': 'Holding Homepage'

    }

    return render(request, 'holding_template/home_content.html', context)

