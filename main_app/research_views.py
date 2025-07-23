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


def research_home(request):
    research = get_object_or_404(Research, admin=request.user)
    total_subject = Subject.objects.filter(organ=research.organ).count()
    total_attendance = AttendanceReport.objects.filter(research=research).count()
    total_present = AttendanceReport.objects.filter(research=research, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present / total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(organ=research.organ)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, research=research).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, research=research).count()
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
        'page_title': 'Research Homepage'

    }
    return render(request, 'research_template/home_content.html', context)


def research_organization_software(request):
    research = get_object_or_404(Research, admin=request.user)
    total_subject = Subject.objects.filter(organ=research.organ).count()
    total_attendance = AttendanceReport.objects.filter(research=research).count()
    total_present = AttendanceReport.objects.filter(research=research, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present / total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.filter(organ=research.organ)
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, research=research).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, research=research).count()
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
        'page_title': 'Research Homepage'

    }
    return render(request, 'research_template/research_organization_software.html', context)


@csrf_exempt
def research_view_attendance(request):
    research = get_object_or_404(Research, admin=request.user)
    if request.method != 'POST':
        organ = get_object_or_404(Organ, id=research.organ.id)
        context = {
            'subjects': Subject.objects.filter(organ=organ),
            'page_title': 'View Attendance'
        }
        return render(request, 'research_template/research_view_attendance.html', context)
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
                attendance__in=attendance, research=research)
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


def research_apply_leave(request):
    form = LeaveReportResearchForm(request.POST or None)
    research = get_object_or_404(Research, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportResearch.objects.filter(research=research),
        'page_title': 'request'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.research = research
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('research_apply_leave'))
            except Exception:
                messages.error(request, "Could not submit")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "research_template/research_apply_leave.html", context)


def research_feedback(request):
    form = FeedbackResearchForm(request.POST or None)
    research = get_object_or_404(Research, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackResearch.objects.filter(research=research),
        'page_title': 'research'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.research = research
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('research_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "research_template/research_feedback.html", context)


def research_view_profile(request):
    research = get_object_or_404(Research, admin=request.user)
    form = ResearchEditForm(request.POST or None, request.FILES or None, instance=research)
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
                admin = research.admin
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
                research.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('research_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "research_template/research_view_profile.html", context)


@csrf_exempt
def research_fcmtoken(request):
    token = request.POST.get('token')
    research_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        research_user.fcm_token = token
        research_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def research_view_notification(request):
    research = get_object_or_404(Research, admin=request.user)
    notifications = NotificationResearch.objects.filter(research=research)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "research_template/research_view_notification.html", context)


def research_view_result(request):
    research = get_object_or_404(Research, admin=request.user)
    results = ResearchResult.objects.filter(research=research)
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request, "research_template/research_view_result.html", context)


def manage_research_change_password_picture(request):
    researchs = CustomUser.objects.filter(user_type=15).filter(email=request.user.email)

    context = {
        'researchs': researchs,
        'page_title': 'بروزرسانی پروفایل'
    }

    return render(request, "research_template/manage_research_change_password_picture.html", context)


def edit_research_user_password(request, research_id):
    research = get_object_or_404(Research, id=research_id)
    form = ResearchFormUserEdit(request.POST or None, instance=research)
    context = {
        'form': form,
        'research_id': research_id,
        'page_title': 'Edit Research'
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
                user = CustomUser.objects.get(id=research.admin.id)
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
                research.session = session
                user.gender = gender
                user.address = address
                research.organ = organ
                user.save()
                research.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_research_user_password', args=[research_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "research_template/edit_research_user_password_template.html", context)


def edit_research_user_picture(request, research_id):
    research = get_object_or_404(Research, id=research_id)
    form = ResearchFormUserEdit(request.POST or None, instance=research)
    context = {
        'form': form,
        'research_id': research_id,
        'page_title': 'Edit Research'
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
                user = CustomUser.objects.get(id=research.admin.id)
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
                research.session = session
                user.gender = gender
                user.address = address
                research.organ = organ
                user.save()
                research.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_research_user_picture', args=[research_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "research_template/edit_research_user_picture_template.html", context)
