import os
import random

from django.contrib import messages
from django.db.models.base import ModelBase
from django.forms.models import ModelFormMetaclass
from django.http import HttpResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse_lazy

import main_app
from main_app.models import CustomUser
from .models import *
from .forms import *
from main_app import models
from main_app import forms

from django.apps import apps
from django.urls import reverse

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from main_app.models import CustomUser
from .my_functions import handle_uploaded_file
from django.views.generic import ListView, CreateView

def all_news(request):
    """
    r = requests.get('https://www.tgju.org/profile/price_dollar_rl')

    soup = BeautifulSoup(r.content, 'html.parser')

    price_tag = soup.find('td', class_='text-left')
    price1 = str(price_tag)[22:24] + ','
    price2 = str(price_tag)[24]
    price3 = str(price_tag)[26:28]
    price = price1 + price2 + price3
    prices = {'price': price}

    context = {
        'prices': prices,
    }
    """
    return render(request, "all_template/all_news.html")


def all_news_1(request):
    return render(request, "all_template/all_news_1.html")


def all_news_2(request):
    return render(request, "all_template/all_news_2.html")


def all_news_3(request):
    return render(request, "all_template/all_news_3.html")


def all_news_4(request):
    return render(request, "all_template/all_news_4.html")


def all_news_5(request):
    return render(request, "all_template/all_news_5.html")


def all_news_6(request):
    return render(request, "all_template/all_news_6.html")


def all_news_7(request):
    return render(request, "all_template/all_news_7.html")


def all_news_8(request):
    return render(request, "all_template/all_news_8.html")


def all_news_9(request):
    return render(request, "all_template/all_news_9.html")


def all_news_10(request):
    return render(request, "all_template/all_news_10.html")


def all_news_11(request):
    return render(request, "all_template/all_news_11.html")


def all_news_12(request):
    return render(request, "all_template/all_news_12.html")


def all_user_download_file(request):
    this_company = ''
    if request.user.user_type == '1':
        this_company = "Admin"
    elif request.user.user_type == '2':
        this_company = "Staff"
    elif request.user.user_type == '3':
        this_company = "Sugar"
    elif request.user.user_type == '4':
        this_company = "Kh"
    elif request.user.user_type == '20':
        this_company = "Person"
    elif request.user.user_type == '5':
        this_company = "Holding"
    elif request.user.user_type == '6':
        this_company = "Piran"
    elif request.user.user_type == '7':
        this_company = "Tomato"
    elif request.user.user_type == '8':
        this_company = "Taraghi"
    elif request.user.user_type == '9':
        this_company = "Tootia"
    elif request.user.user_type == '10':
        this_company = "Drug"
    elif request.user.user_type == '11':
        this_company = "Gen"
    elif request.user.user_type == '12':
        this_company = "Iron"
    elif request.user.user_type == '13':
        this_company = "Ptro"
    elif request.user.user_type == '14':
        this_company = "Agriculture"
    elif request.user.user_type == '15':
        this_company = "research"

    USER_TYPE = (
        ("HOD", "HOD"),
        ("Staff", "Staff"),
        ('پرسون', "Person",),  # اضافه کردن نوع کاربر جدید
        ('گروه توسعه صنایع شهد آذربایجان', "Holding",),  # اضافه کردن نوع کاربر جدید
        ('قند ارومیه', "Sugar",),
        ('قند خوی', "Kh"),  # اضافه کردن نوع کاربر جدید
        ('قند پیرانشهر', "Piran",),  # اضافه کردن نوع کاربر جدید
        ('گلفام', "Tomato",),  # اضافه کردن نوع کاربر جدید
        ('فروشگاه های زنجیره ای ترقی', "Taraghi",),  # اضافه کردن نوع کاربر جدید
        ('صنایع توسعه شهد توتیا', "Tootia",),  # اضافه کردن نوع کاربر جدید
        ('گلفام دارو', "Drug",),  # اضافه کردن نوع کاربر جدید
        ('داروگستر ساوا شفاژن', "Gen",),  # اضافه کردن نوع کاربر جدید
        ('صنایع ذوب آهن شمالغرب', "Iron",),  # اضافه کردن نوع کاربر جدید
        ('پتروشیمی', "Ptro",),  # اضافه کردن نوع کاربر جدید
        ('تحقیقات و خدمات کشاورزی و بهزراعی آذربایجان غربی', "Agriculture",),  # اضافه کردن نوع کاربر جدید
        ('تحقیقات و خدمات فنی مکانیزه چغندر قند ارومیه', "research",),  # اضافه کردن نوع کاربر جدید
    )

    for i in USER_TYPE:
        if i[1] == this_company:
            this_company_2 = i[0]

    # files = []
    # for filename in os.listdir("main_app/static/upload/" + this_company + '/' + request.user.email + '/'):
    #    file_index = {}
    #    file_path = 'upload/' + this_company + '/' + request.user.email + '/' + filename
    #    file_index['path'] = file_path
    #    file_index['name'] = filename
    #    file_index['person'] = files
    #    files.append(file_index)

    student_files = Student.objects.all().filter(company=this_company_2, email=request.user.email)

    JALALI_DATE = (
        ('دی 1403', '101'),
        ('بهمن 1403', '102'),
        ('اسفند 1403', '103'),
        ('فروردین 1404', '104'),
        ('اردیبهشت 1404', '105'),
        ('خرداد 1404', '106'),
        ('تیر 1404', '107'),
        ('مرداد 1404', '108'),
        ('شهریور 1404', '109'),
        ('مهر 1404', '110'),
        ('آبان 1404', '111'),
        ('آذر 1404', '112'),
        ('دی 1404', '113'),
        ('بهمن 1404', '114'),
        ('اسفند 1404', '115'),
        ('فروردین 1405', '116'),
        ('اردیبهشت 1405', '117'),
        ('خرداد 1405', '118'),
    )

    student_files_ordered = student_files.order_by('-month_counter')
    context = {
        'student_files': student_files_ordered,
    }

    print('request.user.user_type: ', request.user.user_type)
    print('request.user.access_level_number: ', request.user.access_level_number)

    try:
        string_number = str(request.user.access_level_number)
        if string_number[1] == '1':
            return render(request, 'all_template/all_user_download_choice_file_template_for_accountant.html', context)
        else:
            return render(request, 'all_template/all_user_download_choice_file_template.html', context)
    except:
        return render(request, 'all_template/all_user_download_choice_file_template.html', context)


@csrf_exempt
def all_fcmtoken(request):
    token = request.POST.get('token')
    all_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        all_user.fcm_token = token
        all_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def all_websites(request):
    """
    r = requests.get('https://www.tgju.org/profile/price_dollar_rl')

    soup = BeautifulSoup(r.content, 'html.parser')

    price_tag = soup.find('td', class_='text-left')
    price1 = str(price_tag)[22:24] + ','
    price2 = str(price_tag)[24]
    price3 = str(price_tag)[26:28]
    price = price1 + price2 + price3
    prices = {'price': price}

    context = {
        'prices': prices,
    }
    """
    return render(request, "all_template/all_websites.html")


def manage_all_change_password_image(request):
    companies = CustomUser.objects.filter(user_type=request.user.user_type).filter(email=request.user.email)

    context = {
        'companies': companies,
        'page_title': 'Manage companies'
    }

    return render(request, "all_template/manage_all_change_password_image.html", context)


def edit_all_user_password(request, all_id):
    return render(request, "all_template/edit_all_user_password_template.html")


"""
def edit_all_user_picture(request, all_id):
    return render(request, "all_template/edit_all_user_picture_template.html")
"""


def edit_all_user_picture(request, all_id):
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

    this_form = this_company[0].upper() + this_company[1:] + "FormUserEdit"
    s1 = "forms." + this_form
    s2 = eval(s1)
    a1 = this_company[0].upper() + this_company[1:]
    a2 = "models." + a1
    a3 = eval(a2)

    form = s2(request.POST)
    context = {
        'form': form,
        'all_id': all_id,
        'page_title': 'Edit Taraghi'
    }

    return render(request, "all_template/edit_all_user_picture_template.html", context)


def reset_password(request):
    return render(request, 'all_template/reset_password.html')


def do_reset_password(request):
    if request.method == 'POST':
        receiver_email = request.POST.get('email')

        random_number = random.randint(10000000, 99999999)

        if NewPasswordUser.objects.all().filter(email=receiver_email).count() == 1:
            models_object = NewPasswordUser.objects.all().get(email=receiver_email)
            models_object.new_password = random_number
            models_object.save()
        elif NewPasswordUser.objects.all().filter(email=receiver_email).count() == 0:
            NewPasswordUser.objects.create(email=receiver_email, new_password=random_number)

        sender_email = "portal@shahdgroup.ir"
        password = "652360@Zxc"

        # تنظیمات پیام ایمیل
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = 'تغییر رمز عبور'

        # متن ایمیل
        body = "این شماره فقط برای شما می باشد و محرمانه است پس آن را برای کسی نفرستید و به کسی نگویید.\nپسورد جدید شما در سامانه پرتال:" + str(
            random_number)
        message.attach(MIMEText(body, 'plain'))

        try:
            # اتصال به سرور SMTP (در اینجا برای Gmail)
            server = smtplib.SMTP('mail.shahdgroup.ir', 587)
            server.starttls()  # ارتباط ایمن
            server.login(sender_email, password)  # ورود به حساب ایمیل سازمانی

            # ارسال ایمیل
            server.sendmail(sender_email, receiver_email, message.as_string())

            print("ایمیل با موفقیت ارسال شد!")

        except Exception as e:
            print(f"خطا در ارسال ایمیل: {e}")

        finally:
            # بستن اتصال به سرور
            server.quit()
        if CustomUser.objects.all().filter(email=receiver_email).exists() == True:
            return render(request, "all_template/reset_password_email_exists.html")
        elif CustomUser.objects.all().filter(email=receiver_email).exists() == False:
            return render(request, "all_template/reset_password_email_not_exists.html")
    return render(request, 'all_template/reset_password.html')


def social_media(request):
    return render(request, 'all_template/social_media.html')


def user_traffic_control(request):
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

    user_traffic_controls = UserLog.objects.all().filter(email=request.user.email)
    user_traffic_controls_ordered = user_traffic_controls.order_by('-login')
    context = {
        'user_traffic_controls': user_traffic_controls_ordered,
    }
    return render(request, 'all_template/user_traffic_control.html', context)


def all_in_progress_1(request):
    return render(request, "all_template/all_in_progress.html")


def all_in_progress_2(request):
    return render(request, "all_template/all_in_progress.html")


def all_in_progress_3(request):
    return render(request, "all_template/all_in_progress.html")


def all_in_progress_4(request):
    return render(request, "all_template/all_in_progress.html")


def all_in_progress_5(request):
    return render(request, "all_template/all_in_progress.html")


def all_in_progress_6(request):
    return render(request, "all_template/all_in_progress.html")


def all_in_progress_7(request):
    return render(request, "all_template/all_in_progress.html")


def all_in_progress_8(request):
    return render(request, "all_template/all_in_progress.html")


def all_in_progress_9(request):
    return render(request, "all_template/all_in_progress.html")


def all_in_progress_10(request):
    return render(request, "all_template/all_in_progress.html")


def organizational_chart(request):
    return render(request, "all_template/organizational_chart.html")


def related_organizations(request):
    return render(request, "all_template/related_organizations.html")


def companies_phone_numbers(request):
    return render(request, "all_template/companies_phone_numbers.html")


def shahd_phone_numbers(request):
    data = CustomUser.objects.all().values('real_person', 'first_name', 'last_name', 'email', 'company',
                                           'company_phone_number', 'internal_company_phone_number')

    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['email'] = i['email']
            this_data['company'] = i['company']
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


def sugar_phone_numbers(request):
    data = CustomUser.objects.filter(user_type=3).values('real_person', 'first_name', 'last_name', 'post', 'email',
                                                         'company', 'company_phone_number',
                                                         'internal_company_phone_number')

    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['post'] = i['post']
            this_data['email'] = i['email']
            this_data['company'] = 'قند ارومیه'
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


def kh_phone_numbers(request):
    data = CustomUser.objects.filter(user_type=4).values('real_person', 'first_name', 'last_name', 'email', 'company',
                                                         'post', 'company_phone_number',
                                                         'internal_company_phone_number')
    print(data)
    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['email'] = i['email']
            this_data['company'] = 'قند خوی'
            this_data['post'] = i['post']
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


def piran_phone_numbers(request):
    data = CustomUser.objects.filter(user_type=6).values('real_person', 'first_name', 'last_name', 'email', 'company',
                                                         'company_phone_number', 'internal_company_phone_number')
    print(data)
    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['email'] = i['email']
            this_data['company'] = i['company']
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


def tomato_phone_numbers(request):
    data = CustomUser.objects.filter(user_type=7).values('real_person', 'first_name', 'last_name', 'email', 'company',
                                                         'company_phone_number', 'internal_company_phone_number')
    print(data)
    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['email'] = i['email']
            this_data['company'] = i['company']
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


def taraghi_phone_numbers(request):
    data = CustomUser.objects.filter(user_type=8).values('real_person', 'first_name', 'last_name', 'email', 'company',
                                                         'company_phone_number', 'internal_company_phone_number')
    print(data)
    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['email'] = i['email']
            this_data['company'] = i['company']
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


def tootia_phone_numbers(request):
    data = CustomUser.objects.filter(user_type=9).values('real_person', 'first_name', 'last_name', 'email', 'company',
                                                         'company_phone_number', 'internal_company_phone_number')
    print(data)
    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['email'] = i['email']
            this_data['company'] = i['company']
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


def drug_phone_numbers(request):
    data = CustomUser.objects.filter(user_type=10).values('real_person', 'first_name', 'last_name', 'email', 'company',
                                                          'company_phone_number', 'internal_company_phone_number')
    print(data)
    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['email'] = i['email']
            this_data['company'] = i['company']
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


def gen_phone_numbers(request):
    data = CustomUser.objects.filter(user_type=11).values('real_person', 'first_name', 'last_name', 'email', 'company',
                                                          'company_phone_number', 'internal_company_phone_number')
    print(data)
    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['email'] = i['email']
            this_data['company'] = i['company']
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


def iron_phone_numbers(request):
    data = CustomUser.objects.filter(user_type=12).values('real_person', 'first_name', 'last_name', 'email', 'company',
                                                          'company_phone_number', 'internal_company_phone_number')
    print(data)
    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['email'] = i['email']
            this_data['company'] = i['company']
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


def ptro_phone_numbers(request):
    data = CustomUser.objects.filter(user_type=13).values('real_person', 'first_name', 'last_name', 'email', 'company',
                                                          'company_phone_number', 'internal_company_phone_number')
    print(data)
    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['email'] = i['email']
            this_data['company'] = i['company']
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


def agriculture_phone_numbers(request):
    data = CustomUser.objects.filter(user_type=15).values('real_person', 'first_name', 'last_name', 'email', 'company',
                                                          'company_phone_number', 'internal_company_phone_number')
    print(data)
    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['email'] = i['email']
            this_data['company'] = i['company']
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


def research_phone_numbers(request):
    data = CustomUser.objects.filter(user_type=15).values('real_person', 'first_name', 'last_name', 'email', 'company',
                                                          'company_phone_number', 'internal_company_phone_number')
    print(data)
    all_data = []
    for i in data:
        this_data = {}
        if i['real_person'] == True:
            this_data['first_name'] = i['first_name']
            this_data['last_name'] = i['last_name']
            this_data['email'] = i['email']
            this_data['company'] = i['company']
            this_data['company_phone_number'] = i['company_phone_number']
            this_data['internal_company_phone_number'] = i['internal_company_phone_number']
            all_data.append(this_data)

    context = {'data': all_data}
    return render(request, "all_template/person_phone_numbers.html", context)


"""
def new_method_creating_personnel(request):
    print(1)
    if request.method == 'POST':
        form = NewMethodCreatingPersonnelForm(request.POST)
        context = {'form': form}
        print(2)
        if form.is_valid():
            print(3)
            personal_number = form.cleaned_data.get('personal_number')
            access_level_number = form.cleaned_data.get('access_level_number')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            passwords_history = form.cleaned_data.get('passwords_history')
            wrong_passwords_number = form.cleaned_data.get('wrong_passwords_number')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            mobile_number = form.cleaned_data.get('mobile_number')
            home_phone_number = form.cleaned_data.get('home_phone_number')
            company_phone_number = form.cleaned_data.get('company_phone_number')
            internal_company_phone_number = form.cleaned_data.get('internal_company_phone_number')
            gender = form.cleaned_data.get('gender')
            home_address = form.cleaned_data.get('home_address')
            company_address = form.cleaned_data.get('company_address')
            main_profile_image = form.cleaned_data.get('main_profile_image')
            all_profile_images = form.cleaned_data.get('all_profile_images')
            company = form.cleaned_data.get('company')
            login_ip_address = form.cleaned_data.get('login_ip_address')
            gregorian_datetime_create = form.cleaned_data.get('gregorian_datetime_create')
            gregorian_datetime_delete = form.cleaned_data.get('gregorian_datetime_delete')
            jalili_datetime_create = form.cleaned_data.get('jalili_datetime_create')
            jalili_datetime_delete = form.cleaned_data.get('jalili_datetime_delete')
            gregorian_logins_datetime = form.cleaned_data.get('gregorian_logins_datetime')
            gregorian_logouts_datetime = form.cleaned_data.get('gregorian_logouts_datetime')
            jalili_logins_datetime = form.cleaned_data.get('jalili_logins_datetime')
            jalili_logouts_datetime = form.cleaned_data.get('jalili_logouts_datetime')
            gregorian_birthday_datetime = form.cleaned_data.get('gregorian_birthday_datetime')
            jalili_birthday_datetime = form.cleaned_data.get('jalili_birthday_datetime')
            files_upload = form.cleaned_data.get('files_upload')
            files_download = form.cleaned_data.get('files_download')
            security_question_answer = form.cleaned_data.get('security_question_answer')
            Actions = form.cleaned_data.get('Actions')
            national_code = form.cleaned_data.get('national_code')
            birth_certificate_number = form.cleaned_data.get('birth_certificate_number')
            work_experience = form.cleaned_data.get('work_experience')
            education = form.cleaned_data.get('education')
            skills = form.cleaned_data.get('skills')
            projects = form.cleaned_data.get('projects')
            awards_and_Honors = form.cleaned_data.get('awards_and_Honors')
            experiences = form.cleaned_data.get('experiences')
            instagram_username = form.cleaned_data.get('instagram_username')
            telegram_id = form.cleaned_data.get('telegram_id')
            whatsapp_id = form.cleaned_data.get('whatsapp_id')
            other_social_media = form.cleaned_data.get('other_social_media')
            house_location_x = form.cleaned_data.get('house_location_x')
            house_location_y = form.cleaned_data.get('house_location_y')
            company_location_x = form.cleaned_data.get('company_location_x')
            company_location_y = form.cleaned_data.get('company_location_y')
            chat_history = form.cleaned_data.get('chat_history')
            residence_country = form.cleaned_data.get('residence_country')
            residence_city = form.cleaned_data.get('residence_city')
            birth_country = form.cleaned_data.get('birth_country')
            birth_city = form.cleaned_data.get('birth_city')
            comments = form.cleaned_data.get('comments')
            documents = form.cleaned_data.get('documents')
            family_numbers = form.cleaned_data.get('family_numbers')
            managers = form.cleaned_data.get('managers')
            try:
                print(4)
                Person.objects.create(personal_number=personal_number)
                print(5)
                user = Person.objects.create(personal_number=personal_number, access_level_number=access_level_number,
                                             username=username, password=password, passwords_history=passwords_history,
                                             wrong_passwords_number=wrong_passwords_number, first_name=first_name,
                                             last_name=last_name, email=email, mobile_number=mobile_number,
                                             home_phone_number=home_phone_number,
                                             company_phone_number=company_phone_number,
                                             internal_company_phone_number=internal_company_phone_number, gender=gender,
                                             home_address=home_address, company_address=company_address,
                                             main_profile_image=main_profile_image,
                                             all_profile_images=all_profile_images, company=company,
                                             login_ip_address=login_ip_address,
                                             gregorian_datetime_create=gregorian_datetime_create,
                                             gregorian_datetime_delete=gregorian_datetime_delete,
                                             jalili_datetime_create=jalili_datetime_create,
                                             jalili_datetime_delete=jalili_datetime_delete,
                                             gregorian_logins_datetime=gregorian_logins_datetime,
                                             gregorian_logouts_datetime=gregorian_logouts_datetime,
                                             jalili_logins_datetime=jalili_logins_datetime,
                                             jalili_logouts_datetime=jalili_logouts_datetime,
                                             gregorian_birthday_datetime=gregorian_birthday_datetime,
                                             jalili_birthday_datetime=jalili_birthday_datetime,
                                             files_upload=files_upload, files_download=files_download,
                                             security_question_answer=security_question_answer, Actions=Actions,
                                             national_code=national_code,
                                             birth_certificate_number=birth_certificate_number,
                                             work_experience=work_experience, education=education, skills=skills,
                                             projects=projects, awards_and_Honors=awards_and_Honors,
                                             experiences=experiences, instagram_username=instagram_username,
                                             telegram_id=telegram_id, whatsapp_id=whatsapp_id,
                                             other_social_media=other_social_media, house_location_x=house_location_x,
                                             house_location_y=house_location_y, company_location_x=company_location_x,
                                             company_location_y=company_location_y, chat_history=chat_history,
                                             residence_country=residence_country, residence_city=residence_city,
                                             birth_country=birth_country, birth_city=birth_city, comments=comments,
                                             documents=documents, family_numbers=family_numbers, managers=managers)
                print(6)
                user.save()
                print(7)

                print()
                print()
                for i in CustomUser.objects.all():
                    print(i.id, i.first_name, i.email,i.password)
                    for j in range(len(i.password)):
                        print(j,' ',end=' ')
                    print()
                    print()

                print("Successfully Update DataBase")
                print()
                print()
            except:
                print("8")
                pass
        else:
            print(55555555555555555555555555)
            context = {'form': NewMethodCreatingPersonnelForm()}
    else:
        context = {'form': NewMethodCreatingPersonnelForm()}

    print(context)
    return render(request, 'all_template/new_method_creating_personnel.html', context)
"""


# views.py


def user_index(request):
    if request.method == 'POST':
        student = StudentForm(request.POST, request.FILES)
        if student.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email_query_set = CustomUser.objects.all().filter(first_name=first_name).filter(
                last_name=last_name).values_list(
                'email',
                flat=True)
            email = ', '.join(str(value) for value in email_query_set)
            email = str(email)



            JALALI_DATE = (
                ('دی 1403', '101'),
                ('بهمن 1403', '102'),
                ('اسفند 1403', '103'),
                ('فروردین 1404', '104'),
                ('اردیبهشت 1404', '105'),
                ('خرداد 1404', '106'),
                ('تیر 1404', '107'),
                ('مرداد 1404', '108'),
                ('شهریور 1404', '109'),
                ('مهر 1404', '110'),
                ('آبان 1404', '111'),
                ('آذر 1404', '112'),
                ('دی 1404', '113'),
                ('بهمن 1404', '114'),
                ('اسفند 1404', '115'),
                ('فروردین 1405', '116'),
                ('اردیبهشت 1405', '117'),
                ('خرداد 1405', '118'),
            )

            month_counter = 0
            for i in JALALI_DATE:
                if i[0] == request.POST.get('jalali_date'):
                    month_counter = int(i[1])

            Student.objects.create(file=request.FILES['file'], company=request.POST.get('company'),
                                   jalali_date=request.POST.get('jalali_date'),
                                   email=email, first_name=request.POST.get('first_name'),
                                   last_name=request.POST.get('last_name'),
                                   month_counter=month_counter
                                   )

            USER_TYPE = (
                ("HOD", "HOD"),
                ("Staff", "Staff"),
                ('پرسون', "Person",),  # اضافه کردن نوع کاربر جدید
                ('گروه توسعه صنایع شهد آذربایجان', "Holding",),  # اضافه کردن نوع کاربر جدید
                ('قند ارومیه', "Sugar",),
                ('قند خوی', "Kh"),  # اضافه کردن نوع کاربر جدید
                ('قند پیرانشهر', "Piran",),  # اضافه کردن نوع کاربر جدید
                ('گلفام', "Tomato",),  # اضافه کردن نوع کاربر جدید
                ('فروشگاه های زنجیره ای ترقی', "Taraghi",),  # اضافه کردن نوع کاربر جدید
                ('صنایع توسعه شهد توتیا', "Tootia",),  # اضافه کردن نوع کاربر جدید
                ('گلفام دارو', "Drug",),  # اضافه کردن نوع کاربر جدید
                ('داروگستر ساوا شفاژن', "Gen",),  # اضافه کردن نوع کاربر جدید
                ('صنایع ذوب آهن شمالغرب', "Iron",),  # اضافه کردن نوع کاربر جدید
                ('پتروشیمی', "Ptro",),  # اضافه کردن نوع کاربر جدید
                ('تحقیقات و خدمات کشاورزی و بهزراعی آذربایجان غربی', "Agriculture",),  # اضافه کردن نوع کاربر جدید
                ('تحقیقات و خدمات فنی مکانیزه چغندر قند ارومیه', "research",),  # اضافه کردن نوع کاربر جدید
            )

            this_company = ''
            for i in USER_TYPE:
                if i[0] == request.POST.get('company'):
                    this_company = i[1]

            if handle_uploaded_file(request.FILES['file'], this_company, first_name,
                                    last_name) == True:
                return render(request, "hod_template/add_file_admin_template_successfully.html", {'form': student})
            else:
                return render(request, "hod_template/add_file_admin_template_error.html", {'form': student})
        else:
            return HttpResponse("error")
    else:
        student = StudentForm()
        return render(request, "hod_template/add_file_admin_template.html", {'form': student})


class DevicePanel(ListView):
    model = Device
    template_name = 'all_template/device_panel.html'
    context_object_name = 'devices'



class DevicePanelCreate(CreateView):
    model = Device
    template_name = 'all_template/device_panel_create.html'
    form_class = DeviceForm
    success_url = reverse_lazy('device_panel')


class DevicePanelSourceDestination(CreateView):
    model = DeviceTransfer
    template_name = 'all_template/device_panel_source_destination.html'
    form_class = DeviceTransferForm

    def get_success_url(self):
        return reverse_lazy('device_panel_source_destination.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transfers'] = DeviceTransfer.objects.all().order_by('-id')
        return context