from django.http import HttpResponse

from main_app.models import CustomUser


def handle_uploaded_file(f, company, first_name, last_name):
    try:
        email_query_set = CustomUser.objects.all().filter(first_name=first_name).filter(last_name=last_name).values_list('email',
                                                                                                              flat=True)
        email = ', '.join(str(value) for value in email_query_set)

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
            if i[0] == company:
                this_company = i[1]
        try:
            with open('main_app/static/upload/' + company + '/' + email + '/' + f.name, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        except:
            pass
        return True
    except:
        return False
