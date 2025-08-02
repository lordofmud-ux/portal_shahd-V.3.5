import json
import os
from datetime import datetime
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt

from .EmailBackend import EmailBackend
from .models import Attendance, Session, Subject, NewPasswordUser, CustomUser, UserLog
from main_app import models
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login
from main_app.models import Flag, UserLog
from django.views.decorators.http import require_POST, require_GET
from .models import NewsViewCount
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from .models import CustomUser
from .models import Device

# Create your views here.

def autocomplete_name(request):
    if 'term' in request.GET:
        qs = CustomUser.objects.filter(first_name__icontains=request.GET.get('term'))
        names = list(qs.values_list('first_name', flat=True).distinct())
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)


def autocomplete_last_name(request):
    if 'term' in request.GET:
        qs = CustomUser.objects.filter(last_name__icontains=request.GET.get('term'))
        last_names = list(qs.values_list('last_name', flat=True).distinct())
        return JsonResponse(last_names, safe=False)
    return JsonResponse([], safe=False)


def export_single_device_excel(request, device_id):
    device = Device.objects.get(id=device_id)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Device Data"
    
    #column width
    column_widths = [10, 10, 15, 40, 10, 10, 20, 20, 30, 10, 10, 5, 10, 20]
    for i, width in enumerate(column_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width

    headers = [
        "نام", "شرکت", "موجود", "توضیحات", "شماره", "مکان",
        "نام مصرف کننده", "نام خانوادگی مصرف کننده", "ایمیل مصرف کننده",
        "دپارتمان", "اتاق", "طبقه", "ساختمان", "قیمت"
    ]
    ws.append(headers)

    ws.append([
        device.name,
        device.company,
        "موجود" if device.exist else "ناموجود",
        device.description,
        device.number,
        device.place,
        device.user_firstname,
        device.user_lastname,
        device.user_email,
        device.department,
        device.room,
        device.floor,
        device.building_name,
        device.price,
    ])

    #styles
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="2A6076", end_color="2A6076", fill_type="solid")
    center_alignment = Alignment(horizontal="center", vertical="center")
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
        cell.border = thin_border

    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=2, column=col_num)
        cell.alignment = center_alignment
        cell.border = thin_border

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    filename = f"device_{device.id}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'

    wb.save(response)
    return response




def test(request):
    if request.user.is_authenticated:
        if request.user.user_type == '2':
            return render(request, 'main_app/test.html')
        else:
            return redirect(reverse("admin_home"))


def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("staff_home"))
        elif request.user.user_type == '4':
            return redirect(reverse("kh_home"))
        elif request.user.user_type == '20':
            return redirect(reverse("person_home"))
        elif request.user.user_type == '5':
            return redirect(reverse("holding_home"))
        elif request.user.user_type == '6':
            return redirect(reverse("piran_home"))
        elif request.user.user_type == '7':
            return redirect(reverse("tomato_home"))
        elif request.user.user_type == '8':
            return redirect(reverse("taraghi_home"))
        elif request.user.user_type == '9':
            return redirect(reverse("tootia_home"))
        elif request.user.user_type == '10':
            return redirect(reverse("drug_home"))
        elif request.user.user_type == '11':
            return redirect(reverse("gen_home"))
        elif request.user.user_type == '12':
            return redirect(reverse("iron_home"))
        elif request.user.user_type == '13':
            return redirect(reverse("ptro_home"))
        elif request.user.user_type == '14':
            return redirect(reverse("agriculture_home"))
        elif request.user.user_type == '15':
            return redirect(reverse("research_home"))
        elif request.user.user_type == '3':
            return redirect(reverse("sugar_home"))
        else:
            return redirect(reverse("sugar_home"))
    return render(request, 'main_app/login.html')


def doLogin(request, **kwargs):
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")
    else:

        # Authenticate user
        # print(NewPasswordUser.objects.filter(email=request.POST.get('email')).values())
        if NewPasswordUser.objects.filter(email=request.POST.get('email')).count() == 1:
            if NewPasswordUser.objects.filter(email=request.POST.get('email')).values_list(
                    'new_password')[0][0] == request.POST.get('password'):
                print(str(NewPasswordUser.objects.filter(email=request.POST.get('email')).values_list(
                    'new_password')[0][0]))
                user = CustomUser.objects.get(email=request.POST.get('email'))
                user.set_password(str(NewPasswordUser.objects.filter(email=request.POST.get('email')).values_list(
                    'new_password')[0][0]))
                user.save()

        # UsernameLog_obj=UsernameLog.objects.create()
        # print(request.POST.get('email'))
        UserLog.objects.create(email=request.POST.get('email'))

        user = EmailBackend.authenticate(request, username=request.POST.get('email'),
                                         password=request.POST.get('password'))
        company = ''
        
        try:
            f = Flag.objects.all().get(id=1)
            f.flag = True
            f.save()
            if user.user_type == '1':
                company = "admin"
            elif user.user_type == '2':
                company = "staff"
            elif user.user_type == '3':
                company = "sugar"
            elif user.user_type == '4':
                company = "kh"
            elif user.user_type == '20':
                company = "person"
            elif user.user_type == '5':
                company = "holding"
            elif user.user_type == '6':
                company = "piran"
            elif user.user_type == '7':
                company = "tomato"
            elif user.user_type == '8':
                company = "taraghi"
            elif user.user_type == '9':
                company = "tootia"
            elif user.user_type == '10':
                company = "drug"
            elif user.user_type == '11':
                company = "gen"
            elif user.user_type == '12':
                company = "iron"
            elif user.user_type == '13':
                company = "ptro"
            elif user.user_type == '14':
                company = "agriculture"
            elif user.user_type == '15':
                company = "research"
                
            user_email = str(user.email)
            user_company = str(company)

            nested_directory = "main_app/static/upload/" + user_company + '/' + user_email
            if os.path.isdir(nested_directory) == True:
                print("hast")
            elif os.path.isdir(nested_directory) == False:
                print("nist")
                os.makedirs(nested_directory)
            if user is not None:
                login(request, user)
                return redirect('all_news')
            else:
                messages.error(request, "Invalid login details")
                return redirect("/")
        except:
            return redirect(reverse("login_page"))


def redirect_user(user):
    """Helper function to redirect based on user type."""
    user_type_redirects = {
        '1': 'admin_home',
        '2': 'staff_home',
        '4': 'kh_home',
        '20': 'person_home',
        '5': 'holding_home',
        '6': 'piran_home',
        '7': 'tomato_home',
        '8': 'taraghi_home',
        '9': 'tootia_home',
        '10': 'drug_home',
        '11': 'gen_home',
        '12': 'iron_home',
        '13': 'ptro_home',
        '14': 'agriculture_home',
        '15': 'research_home',
        '3': 'sugar_home',

    }
    return redirect(reverse(user_type_redirects.get(user.user_type, 'sugar_home')))


def logout_user(request):

    email = str(request.user.email)
    print(datetime.now())
    print(datetime.now())
    print(datetime.now())
    print(datetime.now())
    UserLog_obj = UserLog.objects.filter(email=email).order_by('-id')[0]
    print(UserLog_obj)
    UserLog_obj.logout = datetime.now()
    UserLog_obj.save()
    print(UserLog_obj)

    if request.user != None:
        logout(request)
    return redirect("/")


@csrf_exempt
def get_attendance(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        attendance = Attendance.objects.filter(subject=subject, session=session)
        attendance_list = []
        for attd in attendance:
            data = {
                "id": attd.id,
                "attendance_date": str(attd.date),
                "session": attd.session.id
            }
            attendance_list.append(data)
        return JsonResponse(json.dumps(attendance_list), safe=False)
    except Exception as e:
        return None


def showFirebaseJS(request):
    data = """
    // Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here, other Firebase libraries
// are not available in the service worker.
importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in
// your app's Firebase config object.
// https://firebase.google.com/docs/web/setup#config-object
firebase.initializeApp({
    apiKey: "AIzaSyBarDWWHTfTMSrtc5Lj3Cdw5dEvjAkFwtM",
    authDomain: "sms-with-django.firebaseapp.com",
    databaseURL: "https://sms-with-django.firebaseio.com",
    projectId: "sms-with-django",
    storageBucket: "sms-with-django.appspot.com",
    messagingSenderId: "945324593139",
    appId: "1:945324593139:web:03fa99a8854bbd38420c86",
    measurementId: "G-2F2RXTL9GT"
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();
messaging.setBackgroundMessageHandler(function (payload) {
    const notification = JSON.parse(payload);
    const notificationOption = {
        body: notification.body,
        icon: notification.icon
    }
    return self.registration.showNotification(payload.notification.title, notificationOption);
});
    """
    return HttpResponse(data, content_type='application/javascript')

@csrf_exempt
@require_POST
def increment_view(request, news_id):
    obj, _ = NewsViewCount.objects.get_or_create(news_id=news_id)
    obj.count += 1
    obj.save()
    return JsonResponse({"count": obj.count})

@require_GET
def get_view_count(request, news_id):
    try:
        obj = NewsViewCount.objects.get(news_id=news_id)
        current = obj.count
    except NewsViewCount.DoesNotExist:
        current = 0
    return JsonResponse({"count": current})

