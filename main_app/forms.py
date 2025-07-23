import datetime
import time

from django import forms
from django.forms.widgets import DateInput, TextInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    USER_TYPE = (
        (20, "پرسون"),
        (5, "گروه توسعه صنایع شهد آذربایجان"),
        (3, "قند ارومیه"),
        (4, "قند خوی"),  # اضافه کردن نوع کاربر جدید
        (6, "قند پیرانشهر"),  # اضافه کردن نوع کاربر جدید
        (7, "گلفام"),  # اضافه کردن نوع کاربر جدید
        (8, "فروشگاه های زنجیره ای ترقی"),  # اضافه کردن نوع کاربر جدید
        (9, "صنایع توسعه شهد توتیا"),  # اضافه کردن نوع کاربر جدید
        (10, "گلفام دارو"),  # اضافه کردن نوع کاربر جدید
        (11, "داروگستر ساوا شفاژن"),  # اضافه کردن نوع کاربر جدید
        (12, "صنایع ذوب آهن شمال غرب"),  # اضافه کردن نوع کاربر جدید
        (13, "پتروشیمی"),  # اضافه کردن نوع کاربر جدید
        (14, "تحقیقات و خدمات کشاورزی و بهزراعی آذربایجان غربی"),  # اضافه کردن نوع کاربر جدید
        (15, "تحقیقات و خدمات فنی مکانیزه چغندر قند ارومیه"),
        (1, "HOD"),
        (2, "Staff"),
    )
    COMPANY_CHOICES = [('Person', 'پرسون'),
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
                       ('nwsi', 'صنایع ذوب آهن شمال غرب'),
                       ('Petrochemical', 'پتروشیمی')]

    post = forms.CharField(required=False)
    real_person = forms.BooleanField(initial=False, required=False)
    device_panel = forms.BooleanField(initial=False, required=False)
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(required=False, choices=[('M', 'آقا'), ('F', 'خانم')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(required=False, widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField(required=False)
    company = forms.ChoiceField(required=True, choices=COMPANY_CHOICES)
    user_type = forms.ChoiceField(required=True, choices=USER_TYPE)
    company_phone_number = forms.CharField(required=False)
    internal_company_phone_number = forms.CharField(required=False)
    hiring_date = forms.DateField(required=False)


    # این فیلدها رو من اضافه کردم، اگه به مشکل خورد پاک بشه
    personal_number = forms.IntegerField(required=False)
    access_level_number = forms.IntegerField(required=False)
    username = forms.CharField(required=False)
    # passwords_history = forms.JSONField(required=False)
    wrong_passwords_number = forms.IntegerField(required=False)
    # email = forms.EmailField(required=False)
    mobile_number = forms.CharField(required=False)
    home_phone_number = forms.CharField(required=False)

    # gender = forms.CharField(required=False)
    home_address = forms.CharField(required=False)
    company_address = forms.CharField(required=False)
    # main_profile_image = forms.ImageField(required=False)
    # all_profile_images = forms.JSONField(required=False)
    # login_ip_address = forms.JSONField(required=False)
    gregorian_datetime_create = forms.DateTimeField(required=False)
    gregorian_datetime_delete = forms.DateTimeField(required=False)
    jalili_datetime_create = forms.DateTimeField(required=False)
    jalili_datetime_delete = forms.DateTimeField(required=False)
    # gregorian_logins_datetime = forms.JSONField(required=False)
    # gregorian_logouts_datetime = forms.JSONField(required=False)
    # jalili_logins_datetime = forms.JSONField(required=False)
    # jalili_logouts_datetime = forms.JSONField(required=False)
    gregorian_birthday_datetime = forms.DateTimeField(required=False)
    jalili_birthday_datetime = forms.DateTimeField(required=False)
    # files_upload = forms.JSONField(required=False)
    # files_download = forms.JSONField(required=False)
    # security_question_answer = forms.JSONField(required=False)
    # Actions = forms.JSONField(required=False)
    national_code = forms.CharField(required=False)
    birth_certificate_number = forms.CharField(required=False)
    # work_experience = forms.JSONField(required=False)
    # education = forms.JSONField(required=False)
    # skills = forms.JSONField(required=False)
    # projects = forms.JSONField(required=False)
    # awards_and_Honors = forms.JSONField(required=False)
    # experiences = forms.JSONField(required=False)
    instagram_username = forms.CharField(required=False)
    telegram_id = forms.CharField(required=False)
    # address = forms.CharField(required=False)
    # other_social_media = forms.JSONField(required=False)
    # house_location_x = forms.CharField(required=False)
    # house_location_y = forms.CharField(required=False)
    # ompany_location_x = forms.CharField(required=False)
    # company_location_y = forms.CharField(required=False)
    # chat_history = forms.JSONField(required=False)
    residence_country = forms.CharField(required=False)
    residence_city = forms.CharField(required=False)
    birth_country = forms.CharField(required=False)
    birth_city = forms.CharField(required=False)
    # comments = forms.JSONField(required=False)
    # documents = forms.JSONField(required=False)
    family_numbers = forms.IntegerField(required=False)

    # managers = forms.JSONField(required=False)


    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "پسورد جدید خود را وارد کنید"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            try:
                print(111)
                print(self.instance.pk)
                print(self.Meta.model.objects.all())
                print(222)
                dbEmail = self.Meta.model.objects.get(
                    id=self.instance.pk).admin.email.lower()
                if dbEmail != formEmail:  # There has been changes
                    if CustomUser.objects.filter(email=formEmail).exists():
                        raise forms.ValidationError("The given email is already registered")
            except:
                print("not successfully, error")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender', 'password', 'profile_pic', 'address','personal_number','post','company','internal_company_phone_number']


class SugarForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(SugarForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Sugar
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class KhForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(KhForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Kh
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session','internal_company_phone_number','personal_number']


class PersonForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False

    class Meta(CustomUserForm.Meta):
        model = Person
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']

    """
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.pk:
            # اگر رکورد در حال ویرایش باشد
            if Person.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("The given email is already registered")
        else:
            if Person.objects.filter(email=email).exists():
                raise forms.ValidationError("The given email is already registered")
        return email
    """


class HoldingForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(HoldingForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Holding
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class PiranForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(PiranForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Piran
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class TomatoForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TomatoForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Tomato
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class TaraghiForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TaraghiForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Taraghi
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class TootiaForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TootiaForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Tootia
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class DrugForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(DrugForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Drug
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class GenForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(GenForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Gen
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class IronForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(IronForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Iron
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class PtroForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(PtroForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Ptro
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class AgricultureForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AgricultureForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Agriculture
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class ResearchForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(ResearchForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Research
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + \
                 ['organ']


class OrganForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(OrganForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Organ


class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ['name', 'staff', 'organ', ]


class SessionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = '__all__'
        widgets = {
            'start_year': DateInput(attrs={'type': 'date'}),
            'end_year': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportStaffForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStaff
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackStaffForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStaff
        fields = ['feedback']


class LeaveReportSugarForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportSugarForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportSugar
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportKhForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportKhForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportKh
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportPersonForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportPersonForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportPerson
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportHoldingForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportHoldingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportHolding
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportPiranForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportPiranForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportPiran
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportTomatoForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportTomatoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportTomato
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportTaraghiForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportTaraghiForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportTaraghi
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportTootiaForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportTootiaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportTootia
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportDrugForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportDrugForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportDrug
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportGenForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportGenForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportGen
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportIronForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportIronForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportIron
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportPtroForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportPtroForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportPtro
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportAgricultureForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportAgricultureForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportAgriculture
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportResearchForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportResearchForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportResearch
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackSugarForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackSugarForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackSugar
        fields = ['feedback']


class FeedbackKhForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackKhForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackKh
        fields = ['feedback']


class FeedbackPersonForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackPersonForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackPerson
        fields = ['feedback']


class FeedbackHoldingForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackHoldingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackHolding
        fields = ['feedback']


class FeedbackPiranForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackPiranForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackPiran
        fields = ['feedback']


class FeedbackTomatoForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(FeedbackTomatoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackTomato
        fields = ['feedback']


class FeedbackTaraghiForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackTaraghiForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackTaraghi
        fields = ['feedback']


class FeedbackTootiaForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackTootiaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackTootia
        fields = ['feedback']


class FeedbackDrugForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackDrugForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackDrug
        fields = ['feedback']


class FeedbackGenForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackGenForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackGen
        fields = ['feedback']


class FeedbackIronForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackIronForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackIron
        fields = ['feedback']


class FeedbackPtroForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackPtroForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackPtro
        fields = ['feedback']


class FeedbackAgricultureForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackAgricultureForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackAgriculture
        fields = ['feedback']


class FeedbackResearchForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackResearchForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackResearch
        fields = ['feedback']


class SugarEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(SugarEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Sugar
        fields = CustomUserForm.Meta.fields


class KhEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(KhEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Kh
        fields = CustomUserForm.Meta.fields


class PersonEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(PersonEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Person
        fields = CustomUserForm.Meta.fields


class HoldingEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(HoldingEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Holding
        fields = CustomUserForm.Meta.fields


class PiranEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(PiranEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Piran
        fields = CustomUserForm.Meta.fields


class TomatoEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TomatoEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Tomato
        fields = CustomUserForm.Meta.fields


class TaraghiEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TaraghiEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Taraghi
        fields = CustomUserForm.Meta.fields


class TootiaEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TootiaEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Tootia
        fields = CustomUserForm.Meta.fields


class DrugEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(DrugEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Drug
        fields = CustomUserForm.Meta.fields


class GenEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(GenEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Gen
        fields = CustomUserForm.Meta.fields


class IronEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(IronEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Iron
        fields = CustomUserForm.Meta.fields


class PtroEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(PtroEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Ptro
        fields = CustomUserForm.Meta.fields


class AgricultureEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AgricultureEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Agriculture
        fields = CustomUserForm.Meta.fields


class ResearchEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(ResearchEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Research
        fields = CustomUserForm.Meta.fields


class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields


class EditResultForm(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SugarResult
        fields = ['session_year', 'subject', 'sugar', 'test', 'exam']


class EditResultFormKh(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormKh, self).__init__(*args, **kwargs)

    class Meta:
        model = KhResult
        fields = ['session_year', 'subject', 'kh', 'test', 'exam']


class EditResultFormPerson(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormPerson, self).__init__(*args, **kwargs)

    class Meta:
        model = PersonResult
        fields = ['session_year', 'subject', 'person', 'test', 'exam']


class EditResultFormHolding(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormHolding, self).__init__(*args, **kwargs)

    class Meta:
        model = HoldingResult
        fields = ['session_year', 'subject', 'holding', 'test', 'exam']


class EditResultFormPiran(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormPiran, self).__init__(*args, **kwargs)

    class Meta:
        model = PiranResult
        fields = ['session_year', 'subject', 'piran', 'test', 'exam']


class EditResultFormTomato(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormTomato, self).__init__(*args, **kwargs)

    class Meta:
        model = TomatoResult
        fields = ['session_year', 'subject', 'tomato', 'test', 'exam']


class EditResultFormTaraghi(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormTaraghi, self).__init__(*args, **kwargs)

    class Meta:
        model = TaraghiResult
        fields = ['session_year', 'subject', 'taraghi', 'test', 'exam']


class EditResultFormTootia(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormTootia, self).__init__(*args, **kwargs)

    class Meta:
        model = TootiaResult
        fields = ['session_year', 'subject', 'tootia', 'test', 'exam']


class EditResultFormDrug(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormDrug, self).__init__(*args, **kwargs)

    class Meta:
        model = DrugResult
        fields = ['session_year', 'subject', 'drug', 'test', 'exam']


class EditResultFormGen(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormGen, self).__init__(*args, **kwargs)

    class Meta:
        model = GenResult
        fields = ['session_year', 'subject', 'gen', 'test', 'exam']


class EditResultFormIron(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormIron, self).__init__(*args, **kwargs)

    class Meta:
        model = IronResult
        fields = ['session_year', 'subject', 'iron', 'test', 'exam']


class EditResultFormPtro(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormPtro, self).__init__(*args, **kwargs)

    class Meta:
        model = PtroResult
        fields = ['session_year', 'subject', 'ptro', 'test', 'exam']


class EditResultFormAgriculture(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormAgriculture, self).__init__(*args, **kwargs)

    class Meta:
        model = AgricultureResult
        fields = ['session_year', 'subject', 'agriculture', 'test', 'exam']


class EditResultFormResearch(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultFormResearch, self).__init__(*args, **kwargs)

    class Meta:
        model = ResearchResult
        fields = ['session_year', 'subject', 'research', 'test', 'exam']


class PersonFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(PersonFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Person
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class HoldingFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(HoldingFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Holding
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class KhFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(KhFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Kh
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class PiranFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(PiranFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Piran
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class StudentForm(forms.Form):
    USER_TYPE = (
        ('گروه توسعه صنایع شهد آذربایجان', 'گروه توسعه صنایع شهد آذربایجان'),
        ('قند ارومیه', 'قند ارومیه'),
        ('قند خوی', 'قند خوی'),  # اضافه کردن نوع کاربر جدید  # اضافه کردن نوع کاربر جدید
        ('قند پیرانشهر', 'قند پیرانشهر'),  # اضافه کردن نوع کاربر جدید
        ('گلفام', 'گلفام'),  # اضافه کردن نوع کاربر جدید
        ('فروشگاه های زنجیره ای ترقی', 'فروشگاه های زنجیره ای ترقی'),  # اضافه کردن نوع کاربر جدید
        ('صنایع توسعه شهد توتیا', 'صنایع توسعه شهد توتیا'),  # اضافه کردن نوع کاربر جدید
        ('گلفام دارو', 'گلفام دارو'),  # اضافه کردن نوع کاربر جدید
        ('داروگستر ساوا شفاژن', 'داروگستر ساوا شفاژن'),  # اضافه کردن نوع کاربر جدید
        ('صنایع ذوب آهن شمالغرب', 'صنایع ذوب آهن شمالغرب'),  # اضافه کردن نوع کاربر جدید
        ('پتروشیمی', 'پتروشیمی'),  # اضافه کردن نوع کاربر جدید
        ('تحقیقات و خدمات کشاورزی و بهزراعی آذربایجان غربی', 'تحقیقات و خدمات کشاورزی و بهزراعی آذربایجان غربی'),
        # اضافه کردن نوع کاربر جدید
        ('تحقیقات و خدمات فنی مکانیزه چغندر قند ارومیه', 'تحقیقات و خدمات فنی مکانیزه چغندر قند ارومیه'),
        # اضافه کردن نوع کاربر جدید
    )

    SUBJECT = (
        ('فیش حقوقی', 'فیش حقوقی'),
        ('غیره', 'غیره'),
    )

    JALALI_DATE = (
        ('دی 1403', 'دی 1403'),
        ('بهمن 1403', 'بهمن 1403'),
        ('اسفند 1403', 'اسفند 1403'),
        ('فروردین 1404', 'فروردین 1404'),
        ('اردیبهشت 1404', 'اردیبهشت 1404'),
        ('خرداد 1404', 'خرداد 1404'),
        ('تیر 1404', 'تیر 1404'),
        ('مرداد 1404', 'مرداد 1404'),
        ('شهریور 1404', 'شهریور 1404'),
        ('مهر 1404', 'مهر 1404'),
        ('آبان 1404', 'آبان 1404'),
        ('آذر 1404', 'آذر 1404'),
        ('دی 1404', 'دی 1404'),
        ('بهمن 1404', 'بهمن 1404'),
        ('اسفند 1404', 'اسفند 1404'),
        ('فروردین 1405', 'فروردین 1405'),
        ('اردیبهشت 1405', 'اردیبهشت 1405'),
        ('خرداد 1405', 'خرداد 1405'),
    )

    company = forms.ChoiceField(choices=USER_TYPE, label=" شرکت مورد نظر را انتخاب کنید")
    first_name = forms.CharField(label="نام پرسنل")
    last_name = forms.CharField(label="نام خانوادگی پرسنل ")
    # email = forms.EmailField(label="ایمیل را وارد کنید")
    # date = forms.DateTimeField(initial=datetime.now,label="تاریخ و زمان میلادی آپلود فایل")
    jalali_date = forms.ChoiceField(choices=JALALI_DATE, label="تاریخ")
    file = forms.FileField(label="فایل را اپلود کنید")
    # file_name = forms.CharField(label="نام فایل را وارد کنید")
    # subject = forms.ChoiceField(choices=SUBJECT, label="موضوع را وارد کنید")


class SugarFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(SugarFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Sugar
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


"""
# all form
class AllForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AllForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = All
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']
"""


class TaraghiFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TaraghiFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Taraghi
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class TomatoFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TomatoFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Tomato
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class TootiaFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TootiaFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Tootia
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class AgricultureFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AgricultureFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Agriculture
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class PtroFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(PtroFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Ptro
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class ResearchFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(ResearchFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Research
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class IronFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(IronFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Iron
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class DrugFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(DrugFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Drug
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class GenFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(GenFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Gen
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


class TaraghiFormUserEdit(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TaraghiFormUserEdit, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Taraghi
        fields = CustomUserForm.Meta.fields + \
                 ['organ', 'session']


"""
class NewMethodCreatingPersonnelForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"

    personal_number = forms.IntegerField(required=False)
    access_level_number = forms.IntegerField(required=False)
    username = forms.CharField(required=False)
    password = forms.CharField(required=False)
    passwords_history = forms.JSONField(required=False)
    wrong_passwords_number = forms.IntegerField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    mobile_number = forms.CharField(required=False)
    home_phone_number = forms.CharField(required=False)
    company_phone_number = forms.CharField(required=False)
    internal_company_phone_number = forms.CharField(required=False)
    gender = forms.CharField(required=False)
    home_address = forms.CharField(required=False)
    company_address = forms.CharField(required=False)
    main_profile_image = forms.ImageField(required=False)
    all_profile_images = forms.JSONField(required=False)
    company = forms.CharField(required=False)
    login_ip_address = forms.JSONField(required=False)
    gregorian_datetime_create = forms.DateTimeField(required=False)
    gregorian_datetime_delete = forms.DateTimeField(required=False)
    jalili_datetime_create = forms.DateTimeField(required=False)
    jalili_datetime_delete = forms.DateTimeField(required=False)
    gregorian_logins_datetime = forms.JSONField(required=False)
    gregorian_logouts_datetime = forms.JSONField(required=False)
    jalili_logins_datetime = forms.JSONField(required=False)
    jalili_logouts_datetime = forms.JSONField(required=False)
    gregorian_birthday_datetime = forms.DateTimeField(required=False)
    jalili_birthday_datetime = forms.DateTimeField(required=False)
    files_upload = forms.JSONField(required=False)
    files_download = forms.JSONField(required=False)
    security_question_answer = forms.JSONField(required=False)
    Actions = forms.JSONField(required=False)
    national_code = forms.CharField(required=False)
    birth_certificate_number = forms.CharField(required=False)
    work_experience = forms.JSONField(required=False)
    education = forms.JSONField(required=False)
    skills = forms.JSONField(required=False)
    projects = forms.JSONField(required=False)
    awards_and_Honors = forms.JSONField(required=False)
    experiences = forms.JSONField(required=False)
    instagram_username = forms.CharField(required=False)
    telegram_id = forms.CharField(required=False)
    whatsapp_id = forms.CharField(required=False)
    other_social_media = forms.JSONField(required=False)
    house_location_x = forms.CharField(required=False)
    house_location_y = forms.CharField(required=False)
    company_location_x = forms.CharField(required=False)
    company_location_y = forms.CharField(required=False)
    chat_history = forms.JSONField(required=False)
    residence_country = forms.CharField(required=False)
    residence_city = forms.CharField(required=False)
    birth_country = forms.CharField(required=False)
    birth_city = forms.CharField(required=False)
    comments = forms.JSONField(required=False)
    documents = forms.JSONField(required=False)
    family_numbers = forms.IntegerField(required=False)
    managers = forms.JSONField(required=False)
"""

"""
class DeviceForm(forms.Form):
    name = forms.CharField(max_length=32, required=False)
    company = forms.CharField(max_length=32, required=False)
    description = forms.CharField(max_length=2048, required=False)
    number = forms.IntegerField(required=False)
    place = forms.CharField(max_length=128, required=False)
    owner = forms.CharField(max_length=32, required=False)
    user = forms.CharField(max_length=32, required=False)
    signature = forms.ImageField(required=False)
    department = forms.CharField(max_length=32, required=False)
    room = forms.CharField(max_length=32, required=False)
    floor = forms.IntegerField(required=False)
    building_unit = forms.IntegerField(required=False)
    price = forms.IntegerField(required=False)
"""


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'
        labels={
            'name':'نام',
            'company': 'شرکت',
            'real':'واقعی',
            'exist':'موجود',
            'description': 'توضیحات',
            'number': 'شماره',
            'place': 'مکان',
            'owner_firstname': 'نام مالک',
            'owner_lastname': 'نام خانوادگی مالک',
            'owner_email': 'ایمیل مالک',
            'user_firstname': 'نام مصرف کننده',
            'user_lastname': 'نام خانوادگی مصرف کننده',
            'user_email': 'ایمیل مصرف کننده',
            'signature': 'امضا مصرف کننده',
            'department': 'دپارتمان',
            'room': 'اتاق',
            'floor': 'طبقه',
            'building_name': 'ساختمان',
            'price': 'قیمت'
        }
        widgets = {
            'name':  TextInput(attrs={'style': 'width: 300px;'}),
            'company': TextInput(attrs={'style': 'width: 300px;'}),
            'real':  TextInput(attrs={'style': 'width: 300px;'}),
            'exist':  TextInput(attrs={'style': 'width: 300px;'}),
            'description':  TextInput(attrs={'style': 'width: 300px;'}),
            'number':  TextInput(attrs={'style': 'width: 300px;'}),
            'place':  TextInput(attrs={'style': 'width: 300px;'}),
            'owner_firstname':  TextInput(attrs={'style': 'width: 300px;'}),
            'owner_lastname':  TextInput(attrs={'style': 'width: 300px;'}),
            'owner_email':  TextInput(attrs={'style': 'width: 300px;'}),
            'user_firstname': TextInput(attrs={'style': 'width: 300px;'}),
            'user_lastname':  TextInput(attrs={'style': 'width: 300px;'}),
            'user_email':  TextInput(attrs={'style': 'width: 300px;'}),
            'signature':  TextInput(attrs={'style': 'width: 300px;'}),
            'department':  TextInput(attrs={'style': 'width: 300px;'}),
            'room':  TextInput(attrs={'style': 'width: 300px;'}),
            'floor':  TextInput(attrs={'style': 'width: 300px;'}),
            'building_name':  TextInput(attrs={'style': 'width: 300px;'}),
            'price':  TextInput(attrs={'style': 'width: 300px;'})
        }


class DeviceTransferForm(forms.ModelForm):
    class Meta:
        model = DeviceTransfer
        fields = '__all__'
        labels = {
            'source_person_first_name': 'نام مبدا',
            'source_person_last_name': 'نام خانوادگی مبدا',
            'source_person_email': 'ایمیل مبدا',
            'destination_person_first_name': 'نام مقصد',
            'destination_person_last_name': 'نام خانوادگی مقصد',
            'destination_person_email': 'ایمیل مقصد',
            'datetime': 'تاریخ انتقال کالا',
            'device_name': 'نام کالا',
            'device_number': 'شماره کالا',
            'transfer_time_price':'قیمت کالا در زمان انتقال'
        }
