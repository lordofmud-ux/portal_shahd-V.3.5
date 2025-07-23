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


def drug_home(request):
    drug = get_object_or_404(Drug, admin=request.user)
    total_subject = Subject.objects.filter(organ=drug.organ).count()
    total_attendance = AttendanceReport.objects.filter(drug=drug).count()
    total_present = AttendanceReport.objects.filter(drug=drug, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present/total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(organ=drug.organ)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, drug=drug).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, drug=drug).count()
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
        'page_title': 'Drug Homepage'

    }
    return render(request, 'drug_template/home_content.html', context)


def drug_organization_software(request):
    drug = get_object_or_404(Drug, admin=request.user)
    total_subject = Subject.objects.filter(organ=drug.organ).count()
    total_attendance = AttendanceReport.objects.filter(drug=drug).count()
    total_present = AttendanceReport.objects.filter(drug=drug, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present/total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(organ=drug.organ)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, drug=drug).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, drug=drug).count()
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
        'page_title': 'Drug Homepage'

    }
    return render(request, 'drug_template/drug_organization_software.html', context)


@ csrf_exempt
def drug_view_attendance(request):
    drug = get_object_or_404(Drug, admin=request.user)
    if request.method != 'POST':
        organ = get_object_or_404(Organ, id=drug.organ.id)
        context = {
            'subjects': Subject.objects.filter(organ=organ),
            'page_title': 'View Attendance'
        }
        return render(request, 'drug_template/drug_view_attendance.html', context)
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
                attendance__in=attendance, drug=drug)
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


def drug_apply_leave(request):
    form = LeaveReportDrugForm(request.POST or None)
    drug = get_object_or_404(Drug, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportDrug.objects.filter(drug=drug),
        'page_title': 'request'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.drug = drug
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('drug_apply_leave'))
            except Exception:
                messages.error(request, "Could not submit")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "drug_template/drug_apply_leave.html", context)


def drug_feedback(request):
    form = FeedbackDrugForm(request.POST or None)
    drug = get_object_or_404(Drug, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackDrug.objects.filter(drug=drug),
        'page_title': 'drug'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.drug = drug
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('drug_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "drug_template/drug_feedback.html", context)


def drug_view_profile(request):
    drug = get_object_or_404(Drug, admin=request.user)
    form = DrugEditForm(request.POST or None, request.FILES or None, instance=drug)
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
                admin = drug.admin
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
                drug.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('drug_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "drug_template/drug_view_profile.html", context)


@csrf_exempt
def drug_fcmtoken(request):
    token = request.POST.get('token')
    drug_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        drug_user.fcm_token = token
        drug_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def drug_view_notification(request):
    drug = get_object_or_404(Drug, admin=request.user)
    notifications = NotificationDrug.objects.filter(drug=drug)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "drug_template/drug_view_notification.html", context)


def drug_view_result(request):
    drug = get_object_or_404(Drug, admin=request.user)
    results = DrugResult.objects.filter(drug=drug)
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request, "drug_template/drug_view_result.html", context)


def manage_drug_change_password_picture(request):
    drugs = CustomUser.objects.filter(user_type=10).filter(email=request.user.email)

    context = {
        'drugs': drugs,
        'page_title': 'بروزرسانی پروفایل'
    }

    return render(request, "drug_template/manage_drug_change_password_picture.html", context)


def edit_drug_user_password(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    form = DrugFormUserEdit(request.POST or None, instance=drug)
    context = {
        'form': form,
        'drug_id': drug_id,
        'page_title': 'Edit Drug'
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
                user = CustomUser.objects.get(id=drug.admin.id)
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
                drug.session = session
                user.gender = gender
                user.address = address
                drug.organ = organ
                user.save()
                drug.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_drug_user_password', args=[drug_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "drug_template/edit_drug_user_password_template.html", context)


def edit_drug_user_picture(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    form = DrugFormUserEdit(request.POST or None, instance=drug)
    context = {
        'form': form,
        'drug_id': drug_id,
        'page_title': 'Edit Drug'
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
                user = CustomUser.objects.get(id=drug.admin.id)
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
                drug.session = session
                user.gender = gender
                user.address = address
                drug.organ = organ
                user.save()
                drug.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_drug_user_picture', args=[drug_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "drug_template/edit_drug_user_picture_template.html", context)
