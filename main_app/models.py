from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class NewsViewCount(models.Model):
    news_id = models.CharField(max_length=255, primary_key=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.news_id}: {self.count}"

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)

        # این کد رو هش میکنه
        user.password = make_password(password)
        # این کد دیگه رمز نمیکنه تو دیتابیس
        # user.password = password
        # ولی باید لاگین رو درست کنم چون اونجا رمز رو تبدیل به هش میکنه بعد مقایسه میکنه، اگر نشد باید کد بالا رو برگردونم به حالت اول

        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return "From " + str(self.start_year) + " to " + str(self.end_year)


class CustomUser(AbstractUser):
    USER_TYPE = (
        (1, "HOD"),
        (2, "Staff"),
        (3, "Sugar"),
        (4, "Kh"),  # اضافه کردن نوع کاربر جدید
        (20, "Person"),  # اضافه کردن نوع کاربر جدید
        (5, "Holding"),  # اضافه کردن نوع کاربر جدید
        (6, "Piran"),  # اضافه کردن نوع کاربر جدید
        (7, "Tomato"),  # اضافه کردن نوع کاربر جدید
        (8, "Taraghi"),  # اضافه کردن نوع کاربر جدید
        (9, "Tootia"),  # اضافه کردن نوع کاربر جدید
        (10, "Drug"),  # اضافه کردن نوع کاربر جدید
        (11, "Gen"),  # اضافه کردن نوع کاربر جدید
        (12, "Iron"),  # اضافه کردن نوع کاربر جدید
        (13, "Ptro"),  # اضافه کردن نوع کاربر جدید
        (14, "Agriculture"),  # اضافه کردن نوع کاربر جدید
        (15, "research"),  # اضافه کردن نوع کاربر جدید

    )
    GENDER = [("M", "Male"), ("F", "Female")]

    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
    COMPANY_CHOICES = (('Person', 'پرسون'),
                       ('ShahdGroup', 'گروه توسعه صنایع شهد آذربایجان'),
                       ('UrmiaSugar', 'قند ارومیه'),
                       ('KhoySugar', 'قند خوی'),
                       ('PiraSugar', 'قند پیرانشهر'),
                       ('TaraghiShop', 'فروشگاه های زنجیره ای ترقی'),
                       ('Golfam', 'گلفام'),
                       ('GolfamDaru', 'گلفام دارو'),
                       ('Tootia', 'صنایع توسعه شهد توتیا'),
                       ('Ssnsco', 'داروگستر ساوا شفاژن'),
                       ('UrmiaResearch', 'تحقیقات و خدمات فنی مکانیزه چغندر قند ارومیه'),
                       ('UrmiaAgriculture', 'تحقیقات و خدمات کشاورزی و بهزراعی آذربایجان غربی'),
                       ('nwsi', 'صنایع ذوب آهن شمالغرب'),
                       ('Petrochemical', 'پتروشیمی'),)

    username = models.CharField(max_length=32, null=True, blank=True)
    real_person = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=32, null=True, blank=True)
    company = models.CharField(max_length=32, choices=COMPANY_CHOICES, null=True, blank=True)
    user_type = models.CharField(default=20, choices=USER_TYPE, max_length=2)
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    position = models.CharField(max_length=32 , null=True , blank=True)
    address = models.TextField(null=True, blank=True)
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # این فیلدها رو من اضافه کردم، اگه به مشکل خورد پاک بشه
    post = models.CharField(max_length=32, null=True, blank=True)
    personal_number = models.IntegerField(null=True, blank=True)

    # رقم اول سمت چپ برای همه یوزر ها 9 است
    # رقم دوم سمت چپ(0 حسابدار نیست)(1 حسابدار است)
    access_level_number = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    # passwords_history = models.JSONField(null=True, blank=True)
    wrong_passwords_number = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    unit = models.CharField(max_length=32, null=True, blank=True)
    hiring_date = models.CharField(max_length= 32 , null=True , blank=True)
    # email = models.EmailField(null=True, blank=True)
    mobile_number = models.CharField(max_length=32, null=True, blank=True)
    home_phone_number = models.CharField(max_length=32, null=True, blank=True)
    company_phone_number = models.CharField(max_length=32, null=True, blank=True)
    internal_company_phone_number = models.CharField(max_length=32, null=True, blank=True)
    # gender = models.CharField(max_length=32, choices=GENDER_CHOICES, null=True, blank=True)
    home_address = models.CharField(max_length=256, null=True, blank=True)
    company_address = models.CharField(max_length=256, null=True, blank=True)
    main_profile_image = models.ImageField(null=True, blank=True)
    # all_profile_images = models.JSONField(null=True, blank=True)
    # login_ip_address = models.JSONField(null=True, blank=True)
    gregorian_datetime_create = models.DateTimeField(null=True, blank=True)
    gregorian_datetime_delete = models.DateTimeField(null=True, blank=True)
    jalili_datetime_create = models.DateTimeField(null=True, blank=True)
    jalili_datetime_delete = models.DateTimeField(null=True, blank=True)
    # gregorian_logins_datetime = models.JSONField(null=True, blank=True)
    # gregorian_logouts_datetime = models.JSONField(null=True, blank=True)
    # jalili_logins_datetime = models.JSONField(null=True, blank=True)
    # jalili_logouts_datetime = models.JSONField(null=True, blank=True)
    gregorian_birthday_datetime = models.DateTimeField(null=True, blank=True)
    jalili_birthday_datetime = models.DateTimeField(null=True, blank=True)
    # files_upload = models.JSONField(null=True, blank=True)
    # files_download = models.JSONField(null=True, blank=True)
    # security_question_answer = models.JSONField(null=True, blank=True)
    # Actions = models.JSONField(null=True, blank=True)
    national_code = models.CharField(max_length=32, null=True, blank=True)
    personel_code = models.CharField(max_length=32, null=True, blank=True)
    birth_certificate_number = models.CharField(max_length=32, null=True, blank=True)
    # work_experience = models.JSONField(null=True, blank=True)
    # education = models.JSONField(null=True, blank=True)
    # skills = models.JSONField(null=True, blank=True)
    # projects = models.JSONField(null=True, blank=True)
    # awards_and_Honors = models.JSONField(null=True, blank=True)
    # experiences = models.JSONField(null=True, blank=True)
    instagram_username = models.CharField(max_length=32, null=True, blank=True)
    telegram_id = models.CharField(max_length=32, null=True, blank=True)
    whatsapp_id = models.CharField(max_length=32, null=True, blank=True)
    # other_social_media = models.JSONField(null=True, blank=True)
    house_location_x = models.CharField(max_length=32, null=True, blank=True)
    house_location_y = models.CharField(max_length=32, null=True, blank=True)
    company_location_x = models.CharField(max_length=32, null=True, blank=True)
    company_location_y = models.CharField(max_length=32, null=True, blank=True)
    # chat_history = models.JSONField(null=True, blank=True)
    residence_country = models.CharField(max_length=32, null=True, blank=True)
    residence_city = models.CharField(max_length=32, null=True, blank=True)
    birth_country = models.CharField(max_length=32, null=True, blank=True)
    birth_city = models.CharField(max_length=32, null=True, blank=True)
    # comments = models.JSONField(null=True, blank=True)
    # documents = models.JSONField(null=True, blank=True)
    family_numbers = models.IntegerField(null=True, blank=True)
    # managers = models.JSONField(null=True, blank=True)
    device_panel = models.BooleanField(default=False, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

   

class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Organ(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Kh(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)





    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Person(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Holding(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Piran(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Tomato(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Taraghi(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Tootia(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Drug(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Gen(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Iron(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Ptro(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Agriculture(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Research(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Sugar(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name


class Staff(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Subject(models.Model):
    name = models.CharField(max_length=120)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, )
    organ = models.ForeignKey(Organ, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AttendanceReport(models.Model):
    sugar = models.ForeignKey(Sugar, on_delete=models.DO_NOTHING)
    kh = models.ForeignKey(Kh, on_delete=models.DO_NOTHING, null=True)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=True)
    holding = models.ForeignKey(Holding, on_delete=models.DO_NOTHING, null=True)
    piran = models.ForeignKey(Piran, on_delete=models.DO_NOTHING, null=True)
    tomato = models.ForeignKey(Tomato, on_delete=models.DO_NOTHING, null=True)
    taraghi = models.ForeignKey(Taraghi, on_delete=models.DO_NOTHING, null=True)
    tootia = models.ForeignKey(Tootia, on_delete=models.DO_NOTHING, null=True)
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, null=True)
    gen = models.ForeignKey(Gen, on_delete=models.DO_NOTHING, null=True)
    iron = models.ForeignKey(Iron, on_delete=models.DO_NOTHING, null=True)
    ptro = models.ForeignKey(Ptro, on_delete=models.DO_NOTHING, null=True)
    agriculture = models.ForeignKey(Agriculture, on_delete=models.DO_NOTHING, null=True)
    research = models.ForeignKey(Research, on_delete=models.DO_NOTHING, null=True)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportSugar(models.Model):
    sugar = models.ForeignKey(Sugar, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportKh(models.Model):
    kh = models.ForeignKey(Kh, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportPerson(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportHolding(models.Model):
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportPiran(models.Model):
    piran = models.ForeignKey(Piran, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportTomato(models.Model):
    tomato = models.ForeignKey(Tomato, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportTaraghi(models.Model):
    taraghi = models.ForeignKey(Taraghi, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportTootia(models.Model):
    tootia = models.ForeignKey(Tootia, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportDrug(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportGen(models.Model):
    gen = models.ForeignKey(Gen, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportIron(models.Model):
    iron = models.ForeignKey(Iron, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportPtro(models.Model):
    ptro = models.ForeignKey(Ptro, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportAgriculture(models.Model):
    agriculture = models.ForeignKey(Agriculture, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportResearch(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackSugar(models.Model):
    sugar = models.ForeignKey(Sugar, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackKh(models.Model):
    kh = models.ForeignKey(Kh, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackPerson(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackHolding(models.Model):
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackPiran(models.Model):
    piran = models.ForeignKey(Piran, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackTomato(models.Model):
    tomato = models.ForeignKey(Tomato, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackTaraghi(models.Model):
    taraghi = models.ForeignKey(Taraghi, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackTootia(models.Model):
    tootia = models.ForeignKey(Tootia, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackDrug(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackGen(models.Model):
    gen = models.ForeignKey(Gen, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackIron(models.Model):
    iron = models.ForeignKey(Iron, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackPtro(models.Model):
    ptro = models.ForeignKey(Ptro, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackAgriculture(models.Model):
    agriculture = models.ForeignKey(Agriculture, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackResearch(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationSugar(models.Model):
    sugar = models.ForeignKey(Sugar, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationKh(models.Model):
    kh = models.ForeignKey(Kh, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationPerson(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationHolding(models.Model):
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationPiran(models.Model):
    piran = models.ForeignKey(Piran, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationTomato(models.Model):
    tomato = models.ForeignKey(Tomato, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationTaraghi(models.Model):
    taraghi = models.ForeignKey(Taraghi, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationTootia(models.Model):
    tootia = models.ForeignKey(Tootia, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationDrug(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationGen(models.Model):
    gen = models.ForeignKey(Gen, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationIron(models.Model):
    iron = models.ForeignKey(Iron, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationPtro(models.Model):
    ptro = models.ForeignKey(Ptro, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationAgriculture(models.Model):
    agriculture = models.ForeignKey(Agriculture, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationResearch(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SugarResult(models.Model):
    sugar = models.ForeignKey(Sugar, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class KhResult(models.Model):
    kh = models.ForeignKey(Kh, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PersonResult(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class HoldingResult(models.Model):
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PiranResult(models.Model):
    piran = models.ForeignKey(Piran, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TomatoResult(models.Model):
    tomato = models.ForeignKey(Tomato, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaraghiResult(models.Model):
    taraghi = models.ForeignKey(Taraghi, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TootiaResult(models.Model):
    tootia = models.ForeignKey(Tootia, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DrugResult(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GenResult(models.Model):
    gen = models.ForeignKey(Gen, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class IronResult(models.Model):
    iron = models.ForeignKey(Iron, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PtroResult(models.Model):
    ptro = models.ForeignKey(Ptro, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AgricultureResult(models.Model):
    agriculture = models.ForeignKey(Agriculture, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResearchResult(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Sugar.objects.create(admin=instance)
        if instance.user_type == 4:
            Kh.objects.create(admin=instance)
        if instance.user_type == 20:
            Person.objects.create(admin=instance)
        if instance.user_type == 5:
            Holding.objects.create(admin=instance)
        if instance.user_type == 6:
            Piran.objects.create(admin=instance)
        if instance.user_type == 7:
            Tomato.objects.create(admin=instance)
        if instance.user_type == 8:
            Taraghi.objects.create(admin=instance)
        if instance.user_type == 9:
            Tootia.objects.create(admin=instance)
        if instance.user_type == 10:
            Drug.objects.create(admin=instance)
        if instance.user_type == 11:
            Gen.objects.create(admin=instance)
        if instance.user_type == 12:
            Iron.objects.create(admin=instance)
        if instance.user_type == 13:
            Ptro.objects.create(admin=instance)
        if instance.user_type == 14:
            Agriculture.objects.create(admin=instance)
        if instance.user_type == 15:
            Research.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.sugar.save()
    if instance.user_type == 4:
        instance.kh.save()
    if instance.user_type == 20:
        instance.person.save()
    if instance.user_type == 5:
        instance.holding.save()
    if instance.user_type == 6:
        instance.piran.save()
    if instance.user_type == 7:
        instance.tomato.save()
    if instance.user_type == 8:
        instance.taraghi.save()
    if instance.user_type == 9:
        instance.agriculturetootia.save()
    if instance.user_type == 10:
        instance.drug.save()
    if instance.user_type == 11:
        instance.gen.save()
    if instance.user_type == 12:
        instance.iron.save()
    if instance.user_type == 13:
        instance.ptro.save()
    if instance.user_type == 14:
        instance.agriculture.save()
    if instance.user_type == 15:
        instance.research.save()


# all model
class All(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Student(models.Model):
    company = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField(default=datetime.today())
    jalali_date = models.CharField(max_length=20, null=True, default='-')
    file = models.FileField()
    file_name = models.CharField(max_length=100, null=True)
    subject = models.CharField(max_length=100, null=True, default='-')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    month_counter = models.IntegerField(null=True, blank=True)


class NewPasswordUser(models.Model):
    email = models.EmailField()
    new_password = models.CharField(max_length=25)


class Flag(models.Model):
    flag = models.BooleanField(default=False)


class UserLog(models.Model):
    email = models.EmailField()
    login = models.DateTimeField(auto_now_add=True)
    logout = models.DateTimeField(null=True, blank=True)
    actions = models.CharField(max_length=255, null=True, blank=True)


"""
class Person(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
    COMPANY_CHOICES = (('ShahdGroup', 'گروه توسعه صنایع شهد آذربایجان'),
                       ('UrmiaSugar', 'چغندر قند ارومیه'),
                       ('KhoySugar', 'قند خوی'),
                       ('PiraSugar', 'قند پیرانشهر'),
                       ('TaraghiShop', 'فروشگاه های زنجیره ای ترقی'),
                       ('Golfam', 'گلفام'),
                       ('GolfamDaru', 'گلفام دارو'),
                       ('Tootia', 'صنایع توسعه شهد توتیا'),
                       ('Ssnsco', 'داروگستر ساوا شفاژن'),
                       ('UrmiaResearch', 'تحقیقات و خدمات فنی مکانیزه چغندر قند ارومیه'),
                       ('UrmiaAgriculture', 'تحقیقات و خدمات کشاورزی و بهزراعی آذربایجان غربی'),
                       ('nwsi', 'صنایع ذوب آهن شمالغرب'),
                       ('Petrochemical', 'پتروشیمی'),)

    personal_number = models.IntegerField(null=True, blank=True)
    access_level_number = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    password = models.CharField(max_length=32, null=True, blank=True)
    passwords_history = models.JSONField(null=True, blank=True)
    wrong_passwords_number = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile_number = models.CharField(max_length=32, null=True, blank=True)
    home_phone_number = models.CharField(max_length=32, null=True, blank=True)
    company_phone_number = models.CharField(max_length=32, null=True, blank=True)
    internal_company_phone_number = models.CharField(max_length=32, null=True, blank=True)
    gender = models.CharField(max_length=32, choices=GENDER_CHOICES,null=True, blank=True)
    home_address = models.CharField(max_length=256, null=True, blank=True)
    company_address = models.CharField(max_length=256, null=True, blank=True)
    main_profile_image = models.ImageField(null=True, blank=True)
    all_profile_images = models.JSONField(null=True, blank=True)
    company = models.CharField(max_length=32, choices=COMPANY_CHOICES,null=True, blank=True)
    login_ip_address = models.JSONField(null=True, blank=True)
    gregorian_datetime_create = models.DateTimeField(null=True, blank=True)
    gregorian_datetime_delete = models.DateTimeField(null=True, blank=True)
    jalili_datetime_create = models.DateTimeField(null=True, blank=True)
    jalili_datetime_delete = models.DateTimeField(null=True, blank=True)
    gregorian_logins_datetime = models.JSONField(null=True, blank=True)
    gregorian_logouts_datetime = models.JSONField(null=True, blank=True)
    jalili_logins_datetime = models.JSONField(null=True, blank=True)
    jalili_logouts_datetime = models.JSONField(null=True, blank=True)
    gregorian_birthday_datetime = models.DateTimeField(null=True, blank=True)
    jalili_birthday_datetime = models.DateTimeField(null=True, blank=True)
    files_upload = models.JSONField(null=True, blank=True)
    files_download = models.JSONField(null=True, blank=True)
    security_question_answer = models.JSONField(null=True, blank=True)
    Actions = models.JSONField(null=True, blank=True)
    national_code = models.CharField(max_length=32, null=True, blank=True)
    birth_certificate_number = models.CharField(max_length=32, null=True, blank=True)
    work_experience = models.JSONField(null=True, blank=True)
    education = models.JSONField(null=True, blank=True)
    skills = models.JSONField(null=True, blank=True)
    projects = models.JSONField(null=True, blank=True)
    awards_and_Honors = models.JSONField(null=True, blank=True)
    experiences = models.JSONField(null=True, blank=True)
    instagram_username = models.CharField(max_length=32, null=True, blank=True)
    telegram_id = models.CharField(max_length=32, null=True, blank=True)
    whatsapp_id = models.CharField(max_length=32, null=True, blank=True)
    other_social_media = models.JSONField(null=True, blank=True)
    house_location_x = models.CharField(max_length=32, null=True, blank=True)
    house_location_y = models.CharField(max_length=32, null=True, blank=True)
    company_location_x = models.CharField(max_length=32, null=True, blank=True)
    company_location_y = models.CharField(max_length=32, null=True, blank=True)
    chat_history = models.JSONField(null=True, blank=True)
    residence_country = models.CharField(max_length=32, null=True, blank=True)
    residence_city = models.CharField(max_length=32, null=True, blank=True)
    birth_country = models.CharField(max_length=32, null=True, blank=True)
    birth_city = models.CharField(max_length=32, null=True, blank=True)
    comments = models.JSONField(null=True, blank=True)
    documents = models.JSONField(null=True, blank=True)
    family_numbers = models.IntegerField(null=True, blank=True)
    managers = models.JSONField(null=True, blank=True)
"""


class Device(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    company = models.CharField(max_length=32, null=True, blank=True)
    real = models.BooleanField(default=True)
    exist = models.BooleanField(default=True)
    description = models.TextField(max_length=2048, null=True, blank=True)
    number = models.IntegerField(unique=True, null=True, blank=True)
    place = models.CharField(max_length=128, null=True, blank=True)
    owner_firstname = models.CharField(max_length=32, null=True, blank=True)
    owner_lastname = models.CharField(max_length=32, null=True, blank=True)
    owner_email = models.CharField(max_length=32, null=True, blank=True)
    user_firstname = models.CharField(max_length=32, null=True, blank=True)
    user_lastname = models.CharField(max_length=32, null=True, blank=True)
    user_email = models.CharField(max_length=32, null=True, blank=True)
    signature = models.ImageField(null=True, blank=True)
    department = models.CharField(max_length=32, null=True, blank=True)
    room = models.CharField(max_length=32, null=True, blank=True)
    floor = models.IntegerField(null=True, blank=True)
    building_name = models.CharField(max_length=32, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('device_panel_create')


class DeviceTransfer(models.Model):
    source_person_first_name = models.CharField(max_length=32, null=True, blank=True)
    source_person_last_name = models.CharField(max_length=32, null=True, blank=True)
    source_person_email = models.CharField(max_length=32, null=True, blank=True)
    destination_person_first_name = models.CharField(max_length=32, null=True, blank=True)
    destination_person_last_name = models.CharField(max_length=32, null=True, blank=True)
    destination_person_email = models.CharField(max_length=32, null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    device_name = models.CharField(max_length=32, null=True, blank=True)
    device_number = models.IntegerField(unique=True, null=True, blank=True)
    transfer_time_price = models.IntegerField(null=True, blank=True)
