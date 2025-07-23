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


def kh_home(request):
    kh = get_object_or_404(Kh, admin=request.user)
    total_subject = Subject.objects.filter(organ=kh.organ).count()
    total_attendance = AttendanceReport.objects.filter(kh=kh).count()
    total_present = AttendanceReport.objects.filter(kh=kh, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present / total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(organ=kh.organ)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, kh=kh).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, kh=kh).count()
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
        'page_title': 'Kh Homepage'

    }
    return render(request, 'kh_template/home_content.html', context)

def kh_organization_software(request):
    kh = get_object_or_404(Kh, admin=request.user)
    total_subject = Subject.objects.filter(organ=kh.organ).count()
    total_attendance = AttendanceReport.objects.filter(kh=kh).count()
    total_present = AttendanceReport.objects.filter(kh=kh, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present / total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(organ=kh.organ)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, kh=kh).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, kh=kh).count()
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
        'page_title': 'Kh Homepage'

    }
    return render(request, 'kh_template/home_content.html', context)



@csrf_exempt
def kh_view_attendance(request):
    kh = get_object_or_404(Kh, admin=request.user)
    if request.method != 'POST':
        organ = get_object_or_404(Organ, id=kh.organ.id)
        context = {
            'subjects': Subject.objects.filter(organ=organ),
            'page_title': 'View Attendance'
        }
        return render(request, 'kh_template/kh_view_attendance.html', context)
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
                attendance__in=attendance, kh=kh)
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


def kh_apply_leave(request):
    form = LeaveReportKhForm(request.POST or None)
    kh = get_object_or_404(Kh, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportKh.objects.filter(kh=kh),
        'page_title': 'request'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.kh = kh
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('kh_apply_leave'))
            except Exception:
                messages.error(request, "Could not submit")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "kh_template/kh_apply_leave.html", context)


def kh_feedback(request):
    form = FeedbackKhForm(request.POST or None)
    kh = get_object_or_404(Kh, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackKh.objects.filter(kh=kh),
        'page_title': 'شرکت قند خوی'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.kh = kh
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('kh_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "kh_template/kh_feedback.html", context)


def kh_view_profile(request):
    kh = get_object_or_404(Kh, admin=request.user)
    form = KhEditForm(request.POST or None, request.FILES or None,
                      instance=kh)
    context = {'form': form,
               'kh': kh,
               'page_title': 'View/Edit Profile',
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                print(form.cleaned_data)
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                unit = form.cleaned_data.get('unit')
                passport = request.FILES.get('profile_pic') or None
                admin = kh.admin
    
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.unit = unit
                admin.address = address
                admin.gender = gender
                admin.save()
                kh.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('kh_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "kh_template/kh_view_profile.html", context)


@csrf_exempt
def kh_fcmtoken(request):
    token = request.POST.get('token')
    kh_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        kh_user.fcm_token = token
        kh_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def kh_view_notification(request):
    kh = get_object_or_404(Kh, admin=request.user)
    notifications = NotificationKh.objects.filter(kh=kh)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "kh_template/kh_view_notification.html", context)


def kh_view_result(request):
    kh = get_object_or_404(Kh, admin=request.user)
    results = KhResult.objects.filter(kh=kh)
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request, "kh_template/kh_view_result.html", context)


def manage_kh_change_password(request):
    khs = CustomUser.objects.filter(user_type=4).filter(email=request.user.email)

    context = {
        'khs': khs,
        'page_title': 'بروزرسانی پروفایل'
    }

    return render(request, "kh_template/manage_kh_change_password.html", context)


def edit_kh_user_password(request, kh_id):
    kh = get_object_or_404(Kh, id=kh_id)
    form = KhFormUserEdit(request.POST or None, instance=kh)
    context = {
        'form': form,
        'kh_id': kh_id,
        'page_title': 'Edit Kh'
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
                user = CustomUser.objects.get(id=kh.admin.id)
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
                kh.session = session
                user.gender = gender
                user.address = address
                kh.organ = organ

                user.save()
                kh.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_kh_user_password', args=[kh_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "kh_template/edit_kh_user_password_template.html", context)


def edit_kh_user_picture(request, kh_id):
    print(request.user.user_type)
    print(Kh)
    print(type(Kh))
    kh = get_object_or_404(Kh, id=kh_id)
    form = KhFormUserEdit(request.POST or None, instance=kh)
    print(3535)
    print(type(KhFormUserEdit))
    context = {
        'form': form,
        'kh_id': kh_id,
        'page_title': 'Edit Kh'
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
                user = CustomUser.objects.get(id=kh.admin.id)
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
                kh.session = session
                user.gender = gender
                user.address = address
                kh.organ = organ
                user.save()
                kh.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_kh_user_picture', args=[kh_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "kh_template/edit_kh_user_picture_template.html", context)
