import json
import math
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


def agriculture_home(request):
    agriculture = get_object_or_404(Agriculture, admin=request.user)
    total_subject = Subject.objects.filter(organ=agriculture.organ).count()
    total_attendance = AttendanceReport.objects.filter(agriculture=agriculture).count()
    total_present = AttendanceReport.objects.filter(agriculture=agriculture, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present/total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(organ=agriculture.organ)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, agriculture=agriculture).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, agriculture=agriculture).count()
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
        'page_title': 'Agriculture Homepage'

    }
    return render(request, 'agriculture_template/home_content.html', context)


def agriculture_organization_software(request):
    agriculture = get_object_or_404(Agriculture, admin=request.user)
    total_subject = Subject.objects.filter(organ=agriculture.organ).count()
    total_attendance = AttendanceReport.objects.filter(agriculture=agriculture).count()
    total_present = AttendanceReport.objects.filter(agriculture=agriculture, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present/total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(organ=agriculture.organ)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, agriculture=agriculture).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, agriculture=agriculture).count()
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
        'page_title': 'Agriculture Homepage'

    }
    return render(request, 'agriculture_template/agriculture_organization_software.html', context)



@ csrf_exempt
def agriculture_view_attendance(request):
    agriculture = get_object_or_404(Agriculture, admin=request.user)
    if request.method != 'POST':
        organ = get_object_or_404(Organ, id=agriculture.organ.id)
        context = {
            'subjects': Subject.objects.filter(organ=organ),
            'page_title': 'View Attendance'
        }
        return render(request, 'agriculture_template/agriculture_view_attendance.html', context)
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
                attendance__in=attendance, agriculture=agriculture)
            json_data = []
            for report in attendance_reports:
                data = {
                    "date":  str(report.attendance.date),
                    "status": report.status
                }
                json_data.append(data)
            return JsonResponse(json.dumps(json_data), safe=False)
        except Exception as e:
            return None


def agriculture_apply_leave(request):
    form = LeaveReportAgricultureForm(request.POST or None)
    agriculture = get_object_or_404(Agriculture, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportAgriculture.objects.filter(agriculture=agriculture),
        'page_title': 'request'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.agriculture = agriculture
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('agriculture_apply_leave'))
            except Exception:
                messages.error(request, "Could not submit")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "agriculture_template/agriculture_apply_leave.html", context)


def agriculture_feedback(request):
    form = FeedbackAgricultureForm(request.POST or None)
    agriculture = get_object_or_404(Agriculture, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackAgriculture.objects.filter(agriculture=agriculture),
        'page_title': 'agriculture'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.agriculture = agriculture
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('agriculture_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "agriculture_template/agriculture_feedback.html", context)


def agriculture_view_profile(request):
    agriculture = get_object_or_404(Agriculture, admin=request.user)
    form = AgricultureEditForm(request.POST or None, request.FILES or None, instance=agriculture)
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
                admin = agriculture.admin
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
                agriculture.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('agriculture_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "agriculture_template/agriculture_view_profile.html", context)


@csrf_exempt
def agriculture_fcmtoken(request):
    token = request.POST.get('token')
    agriculture_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        agriculture_user.fcm_token = token
        agriculture_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def agriculture_view_notification(request):
    agriculture = get_object_or_404(Agriculture, admin=request.user)
    notifications = NotificationAgriculture.objects.filter(agriculture=agriculture)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "agriculture_template/agriculture_view_notification.html", context)


def agriculture_view_result(request):
    agriculture = get_object_or_404(Agriculture, admin=request.user)
    results = AgricultureResult.objects.filter(agriculture=agriculture)
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request, "agriculture_template/agriculture_view_result.html", context)


def manage_agriculture_change_password_picture(request):
    agricultures = CustomUser.objects.filter(user_type=14).filter(email=request.user.email)

    context = {
        'agricultures': agricultures,
        'page_title': 'بروزرسانی پروفایل'
    }

    return render(request, "agriculture_template/manage_agriculture_change_password_picture.html", context)


def edit_agriculture_user_password(request, agriculture_id):
    agriculture = get_object_or_404(Agriculture, id=agriculture_id)
    form = AgricultureFormUserEdit(request.POST or None, instance=agriculture)
    context = {
        'form': form,
        'agriculture_id': agriculture_id,
        'page_title': 'Edit Agriculture'
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
                user = CustomUser.objects.get(id=agriculture.admin.id)
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
                agriculture.session = session
                user.gender = gender
                user.address = address
                agriculture.organ = organ
                user.save()
                agriculture.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_agriculture_user_password', args=[agriculture_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "agriculture_template/edit_agriculture_user_password_template.html", context)


def edit_agriculture_user_picture(request, agriculture_id):
    agriculture = get_object_or_404(Agriculture, id=agriculture_id)
    form = AgricultureFormUserEdit(request.POST or None, instance=agriculture)
    context = {
        'form': form,
        'agriculture_id': agriculture_id,
        'page_title': 'Edit Agriculture'
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
                user = CustomUser.objects.get(id=agriculture.admin.id)
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
                agriculture.session = session
                user.gender = gender
                user.address = address
                agriculture.organ = organ
                user.save()
                agriculture.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_agriculture_user_picture', args=[agriculture_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "agriculture_template/edit_agriculture_user_picture_template.html", context)
