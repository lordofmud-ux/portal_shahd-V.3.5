import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

import main_app.models
from .forms import *
from .models import *
from .tomato_views import tomato_view_attendance
from .taraghi_views import taraghi_view_attendance

# admin upload file
from main_app.my_functions import handle_uploaded_file
from main_app.forms import StudentForm

import os
from django.apps import apps
from django.http import JsonResponse


def admin_home(request):
    total_staff = Staff.objects.all().count()
    total_sugars = Sugar.objects.all().count()
    total_khs = Kh.objects.all().count()
    total_persons = Person.objects.all().count()
    total_holdings = Holding.objects.all().count()
    total_pirans = Piran.objects.all().count()
    total_tomatos = Tomato.objects.all().count()
    total_taraghis = Taraghi.objects.all().count()
    total_tootias = Tootia.objects.all().count()
    total_drugs = Drug.objects.all().count()
    total_gens = Gen.objects.all().count()
    total_irons = Iron.objects.all().count()
    total_ptros = Ptro.objects.all().count()
    total_agricultures = Agriculture.objects.all().count()
    total_researchs = Research.objects.all().count()
    subjects = Subject.objects.all()
    total_subject = subjects.count()
    total_organ = Organ.objects.all().count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        subject_list.append(subject.name[:7])
        attendance_list.append(attendance_count)

    # Total Subjects and sugars in Each Organ
    organ_all = Organ.objects.all()
    organ_name_list = []
    subject_count_list = []
    sugar_count_list_in_organ = []
    kh_count_list_in_organ = []
    person_count_list_in_organ = []
    holding_count_list_in_organ = []
    piran_count_list_in_organ = []
    tomato_count_list_in_organ = []
    taraghi_count_list_in_organ = []
    tootia_count_list_in_organ = []
    drug_count_list_in_organ = []
    gen_count_list_in_organ = []
    iron_count_list_in_organ = []
    ptro_count_list_in_organ = []
    agriculture_count_list_in_organ = []
    research_count_list_in_organ = []

    for organ in organ_all:
        subjects = Subject.objects.filter(organ_id=organ.id).count()
        sugars = Sugar.objects.filter(organ_id=organ.id).count()
        khs = Kh.objects.filter(organ_id=organ.id).count()
        persons = Person.objects.filter(organ_id=organ.id).count()
        holdings = Holding.objects.filter(organ_id=organ.id).count()
        pirans = Piran.objects.filter(organ_id=organ.id).count()
        tomatos = Tomato.objects.filter(organ_id=organ.id).count()
        taraghis = Taraghi.objects.filter(organ_id=organ.id).count()
        tootias = Tootia.objects.filter(organ_id=organ.id).count()
        drugs = Drug.objects.filter(organ_id=organ.id).count()
        gens = Gen.objects.filter(organ_id=organ.id).count()
        irons = Iron.objects.filter(organ_id=organ.id).count()
        ptros = Ptro.objects.filter(organ_id=organ.id).count()
        agricultures = Agriculture.objects.filter(organ_id=organ.id).count()
        researchs = Research.objects.filter(organ_id=organ.id).count()
        organ_name_list.append(organ.name)
        subject_count_list.append(subjects)
        sugar_count_list_in_organ.append(sugars)
        kh_count_list_in_organ.append(khs)
        person_count_list_in_organ.append(persons)
        holding_count_list_in_organ.append(holdings)
        piran_count_list_in_organ.append(pirans)
        tomato_count_list_in_organ.append(tomatos)
        taraghi_count_list_in_organ.append(taraghis)
        tootia_count_list_in_organ.append(tootias)
        drug_count_list_in_organ.append(drugs)
        gen_count_list_in_organ.append(gens)
        iron_count_list_in_organ.append(irons)
        ptro_count_list_in_organ.append(ptros)
        agriculture_count_list_in_organ.append(agricultures)
        research_count_list_in_organ.append(researchs)

    subject_all = Subject.objects.all()
    subject_list = []
    sugar_count_list_in_subject = []
    kh_count_list_in_subject = []
    person_count_list_in_subject = []
    holding_count_list_in_subject = []
    piran_count_list_in_subject = []
    tomato_count_list_in_subject = []
    taraghi_count_list_in_subject = []
    tootia_count_list_in_subject = []
    drug_count_list_in_subject = []
    gen_count_list_in_subject = []
    iron_count_list_in_subject = []
    ptro_count_list_in_subject = []
    agriculture_count_list_in_subject = []
    research_count_list_in_subject = []

    for subject in subject_all:
        organ = Organ.objects.get(id=subject.organ.id)
        sugar_count = Sugar.objects.filter(organ_id=organ.id).count()
        kh_count = Kh.objects.filter(organ_id=organ.id).count()
        person_count = Person.objects.filter(organ_id=organ.id).count()
        holding_count = Holding.objects.filter(organ_id=organ.id).count()
        piran_count = Piran.objects.filter(organ_id=organ.id).count()
        tomato_count = Tomato.objects.filter(organ_id=organ.id).count()
        taraghi_count = Taraghi.objects.filter(organ_id=organ.id).count()
        tootia_count = Tootia.objects.filter(organ_id=organ.id).count()
        drug_count = Drug.objects.filter(organ_id=organ.id).count()
        gen_count = Gen.objects.filter(organ_id=organ.id).count()
        iron_count = Iron.objects.filter(organ_id=organ.id).count()
        ptro_count = Ptro.objects.filter(organ_id=organ.id).count()
        agriculture_count = Agriculture.objects.filter(organ_id=organ.id).count()
        research_count = Research.objects.filter(organ_id=organ.id).count()
        subject_list.append(subject.name)
        sugar_count_list_in_subject.append(sugar_count)
        kh_count_list_in_subject.append(kh_count)
        person_count_list_in_subject.append(person_count)
        holding_count_list_in_subject.append(holding_count)
        piran_count_list_in_subject.append(piran_count)
        tomato_count_list_in_subject.append(tomato_count)
        taraghi_count_list_in_subject.append(taraghi_count)
        tootia_count_list_in_subject.append(tootia_count)
        drug_count_list_in_subject.append(drug_count)
        gen_count_list_in_subject.append(gen_count)
        iron_count_list_in_subject.append(iron_count)
        ptro_count_list_in_subject.append(ptro_count)
        agriculture_count_list_in_subject.append(agriculture_count)
        research_count_list_in_subject.append(research_count)

    # For Sugars
    sugar_attendance_present_list = []
    sugar_attendance_leave_list = []
    sugar_name_list = []

    sugars = Sugar.objects.all()
    for sugar in sugars:
        attendance = AttendanceReport.objects.filter(sugar_id=sugar.id, status=True).count()
        absent = AttendanceReport.objects.filter(sugar_id=sugar.id, status=False).count()
        leave = LeaveReportSugar.objects.filter(sugar_id=sugar.id, status=1).count()
        sugar_attendance_present_list.append(attendance)
        sugar_attendance_leave_list.append(leave + absent)
        sugar_name_list.append(sugar.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_sugars': total_sugars,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'sugar_attendance_present_list': sugar_attendance_present_list,
        'sugar_attendance_leave_list': sugar_attendance_leave_list,
        "sugar_name_list": sugar_name_list,
        "sugar_count_list_in_subject": sugar_count_list_in_subject,
        "sugar_count_list_in_organ": sugar_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    # For khoy
    kh_attendance_present_list = []
    kh_attendance_leave_list = []
    kh_name_list = []

    khs = Kh.objects.all()
    for kh in khs:
        attendance = AttendanceReport.objects.filter(kh_id=kh.id, status=True).count()
        absent = AttendanceReport.objects.filter(kh_id=kh.id, status=False).count()
        leave = LeaveReportKh.objects.filter(kh_id=kh.id, status=1).count()
        kh_attendance_present_list.append(attendance)
        kh_attendance_leave_list.append(leave + absent)
        kh_name_list.append(kh.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_khs': total_khs,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'kh_attendance_present_list': kh_attendance_present_list,
        'kh_attendance_leave_list': kh_attendance_leave_list,
        "kh_name_list": kh_name_list,
        "kh_count_list_in_subject": kh_count_list_in_subject,
        "kh_count_list_in_organ": kh_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

    # For person
    person_attendance_present_list = []
    person_attendance_leave_list = []
    person_name_list = []

    persons = Person.objects.all()
    for person in persons:
        attendance = AttendanceReport.objects.filter(person_id=person.id, status=True).count()
        absent = AttendanceReport.objects.filter(person_id=person.id, status=False).count()
        leave = LeaveReportPerson.objects.filter(person_id=person.id, status=1).count()
        person_attendance_present_list.append(attendance)
        person_attendance_leave_list.append(leave + absent)
        person_name_list.append(person.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_persons': total_persons,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'person_attendance_present_list': person_attendance_present_list,
        'person_attendance_leave_list': person_attendance_leave_list,
        "person_name_list": person_name_list,
        "person_count_list_in_subject": person_count_list_in_subject,
        "person_count_list_in_organ": person_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

    # For holding
    holding_attendance_present_list = []
    holding_attendance_leave_list = []
    holding_name_list = []

    holdings = Holding.objects.all()
    for holding in holdings:
        attendance = AttendanceReport.objects.filter(holding_id=holding.id, status=True).count()
        absent = AttendanceReport.objects.filter(holding_id=holding.id, status=False).count()
        leave = LeaveReportHolding.objects.filter(holding_id=holding.id, status=1).count()
        holding_attendance_present_list.append(attendance)
        holding_attendance_leave_list.append(leave + absent)
        holding_name_list.append(holding.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_holdings': total_holdings,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'holding_attendance_present_list': holding_attendance_present_list,
        'holding_attendance_leave_list': holding_attendance_leave_list,
        "holding_name_list": holding_name_list,
        "holding_count_list_in_subject": holding_count_list_in_subject,
        "holding_count_list_in_organ": holding_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

    # For piran

    piran_attendance_present_list = []
    piran_attendance_leave_list = []
    piran_name_list = []

    pirans = Piran.objects.all()
    for piran in pirans:
        attendance = AttendanceReport.objects.filter(piran_id=piran.id, status=True).count()
        absent = AttendanceReport.objects.filter(piran_id=piran.id, status=False).count()
        leave = LeaveReportPiran.objects.filter(piran_id=piran.id, status=1).count()
        piran_attendance_present_list.append(attendance)
        piran_attendance_leave_list.append(leave + absent)
        piran_name_list.append(piran.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_pirans': total_pirans,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'piran_attendance_present_list': piran_attendance_present_list,
        'piran_attendance_leave_list': piran_attendance_leave_list,
        "piran_name_list": piran_name_list,
        "piran_count_list_in_subject": piran_count_list_in_subject,
        "piran_count_list_in_organ": piran_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

    # For tomato

    tomato_attendance_present_list = []
    tomato_attendance_leave_list = []
    tomato_name_list = []

    tomatos = Tomato.objects.all()
    for tomato in tomatos:
        attendance = AttendanceReport.objects.filter(tomato_id=tomato.id, status=True).count()
        absent = AttendanceReport.objects.filter(tomato_id=tomato.id, status=False).count()
        leave = LeaveReportTomato.objects.filter(tomato_id=tomato.id, status=1).count()
        tomato_attendance_present_list.append(attendance)
        tomato_attendance_leave_list.append(leave + absent)
        tomato_name_list.append(tomato.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_tomatos': total_tomatos,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'tomato_attendance_present_list': tomato_attendance_present_list,
        'tomato_attendance_leave_list': tomato_attendance_leave_list,
        "tomato_name_list": tomato_name_list,
        "tomato_count_list_in_subject": tomato_count_list_in_subject,
        "tomato_count_list_in_organ": tomato_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

    # For taraghi

    taraghi_attendance_present_list = []
    taraghi_attendance_leave_list = []
    taraghi_name_list = []

    taraghis = Taraghi.objects.all()
    for taraghi in taraghis:
        attendance = AttendanceReport.objects.filter(taraghi_id=taraghi.id, status=True).count()
        absent = AttendanceReport.objects.filter(taraghi_id=taraghi.id, status=False).count()
        leave = LeaveReportTaraghi.objects.filter(taraghi_id=taraghi.id, status=1).count()
        taraghi_attendance_present_list.append(attendance)
        taraghi_attendance_leave_list.append(leave + absent)
        taraghi_name_list.append(taraghi.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_taraghis': total_taraghis,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'taraghi_attendance_present_list': taraghi_attendance_present_list,
        'taraghi_attendance_leave_list': taraghi_attendance_leave_list,
        "taraghi_name_list": taraghi_name_list,
        "taraghi_count_list_in_subject": taraghi_count_list_in_subject,
        "taraghi_count_list_in_organ": taraghi_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

    # For tootia

    tootia_attendance_present_list = []
    tootia_attendance_leave_list = []
    tootia_name_list = []

    tootias = Tootia.objects.all()
    for tootia in tootias:
        attendance = AttendanceReport.objects.filter(tootia_id=tootia.id, status=True).count()
        absent = AttendanceReport.objects.filter(tootia_id=tootia.id, status=False).count()
        leave = LeaveReportTootia.objects.filter(tootia_id=tootia.id, status=1).count()
        tootia_attendance_present_list.append(attendance)
        tootia_attendance_leave_list.append(leave + absent)
        tootia_name_list.append(tootia.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_tootias': total_tootias,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'tootia_attendance_present_list': tootia_attendance_present_list,
        'tootia_attendance_leave_list': tootia_attendance_leave_list,
        "tootia_name_list": tootia_name_list,
        "tootia_count_list_in_subject": tootia_count_list_in_subject,
        "tootia_count_list_in_organ": tootia_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

    # For drug

    drug_attendance_present_list = []
    drug_attendance_leave_list = []
    drug_name_list = []

    drugs = Drug.objects.all()
    for drug in drugs:
        attendance = AttendanceReport.objects.filter(drug_id=drug.id, status=True).count()
        absent = AttendanceReport.objects.filter(drug_id=drug.id, status=False).count()
        leave = LeaveReportDrug.objects.filter(drug_id=drug.id, status=1).count()
        drug_attendance_present_list.append(attendance)
        drug_attendance_leave_list.append(leave + absent)
        drug_name_list.append(drug.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_drugs': total_drugs,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'drug_attendance_present_list': drug_attendance_present_list,
        'drug_attendance_leave_list': drug_attendance_leave_list,
        "drug_name_list": drug_name_list,
        "drug_count_list_in_subject": drug_count_list_in_subject,
        "drug_count_list_in_organ": drug_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

    # For gen

    gen_attendance_present_list = []
    gen_attendance_leave_list = []
    gen_name_list = []

    gens = Gen.objects.all()
    for gen in gens:
        attendance = AttendanceReport.objects.filter(gen_id=gen.id, status=True).count()
        absent = AttendanceReport.objects.filter(gen_id=gen.id, status=False).count()
        leave = LeaveReportGen.objects.filter(gen_id=gen.id, status=1).count()
        gen_attendance_present_list.append(attendance)
        gen_attendance_leave_list.append(leave + absent)
        gen_name_list.append(gen.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_gens': total_gens,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'gen_attendance_present_list': gen_attendance_present_list,
        'gen_attendance_leave_list': gen_attendance_leave_list,
        "gen_name_list": gen_name_list,
        "gen_count_list_in_subject": gen_count_list_in_subject,
        "gen_count_list_in_organ": gen_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

    # For iron

    iron_attendance_present_list = []
    iron_attendance_leave_list = []
    iron_name_list = []

    irons = Iron.objects.all()
    for iron in irons:
        attendance = AttendanceReport.objects.filter(iron_id=iron.id, status=True).count()
        absent = AttendanceReport.objects.filter(iron_id=iron.id, status=False).count()
        leave = LeaveReportIron.objects.filter(iron_id=iron.id, status=1).count()
        iron_attendance_present_list.append(attendance)
        iron_attendance_leave_list.append(leave + absent)
        iron_name_list.append(iron.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_irons': total_irons,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'iron_attendance_present_list': iron_attendance_present_list,
        'iron_attendance_leave_list': iron_attendance_leave_list,
        "iron_name_list": iron_name_list,
        "iron_count_list_in_subject": iron_count_list_in_subject,
        "iron_count_list_in_organ": iron_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

    # For ptro

    ptro_attendance_present_list = []
    ptro_attendance_leave_list = []
    ptro_name_list = []

    ptros = Ptro.objects.all()
    for ptro in ptros:
        attendance = AttendanceReport.objects.filter(ptro_id=ptro.id, status=True).count()
        absent = AttendanceReport.objects.filter(ptro_id=ptro.id, status=False).count()
        leave = LeaveReportPtro.objects.filter(ptro_id=ptro.id, status=1).count()
        ptro_attendance_present_list.append(attendance)
        ptro_attendance_leave_list.append(leave + absent)
        ptro_name_list.append(ptro.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_ptros': total_ptros,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'ptro_attendance_present_list': ptro_attendance_present_list,
        'ptro_attendance_leave_list': ptro_attendance_leave_list,
        "ptro_name_list": ptro_name_list,
        "ptro_count_list_in_subject": ptro_count_list_in_subject,
        "ptro_count_list_in_organ": ptro_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

    # For agriculture

    agriculture_attendance_present_list = []
    agriculture_attendance_leave_list = []
    agriculture_name_list = []

    agricultures = Agriculture.objects.all()
    for agriculture in agricultures:
        attendance = AttendanceReport.objects.filter(agriculture_id=agriculture.id, status=True).count()
        absent = AttendanceReport.objects.filter(agriculture_id=agriculture.id, status=False).count()
        leave = LeaveReportAgriculture.objects.filter(agriculture_id=agriculture.id, status=1).count()
        agriculture_attendance_present_list.append(attendance)
        agriculture_attendance_leave_list.append(leave + absent)
        agriculture_name_list.append(agriculture.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_agricultures': total_agricultures,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'agriculture_attendance_present_list': agriculture_attendance_present_list,
        'agriculture_attendance_leave_list': agriculture_attendance_leave_list,
        "agriculture_name_list": agriculture_name_list,
        "agriculture_count_list_in_subject": agriculture_count_list_in_subject,
        "agriculture_count_list_in_organ": agriculture_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

    # For research

    research_attendance_present_list = []
    research_attendance_leave_list = []
    research_name_list = []

    researchs = Research.objects.all()
    for research in researchs:
        attendance = AttendanceReport.objects.filter(research_id=research.id, status=True).count()
        absent = AttendanceReport.objects.filter(research_id=research.id, status=False).count()
        leave = LeaveReportResearch.objects.filter(research_id=research.id, status=1).count()
        research_attendance_present_list.append(attendance)
        research_attendance_leave_list.append(leave + absent)
        research_name_list.append(research.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_researchs': total_researchs,
        'total_staff': total_staff,
        'total_organ': total_organ,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'research_attendance_present_list': research_attendance_present_list,
        'research_attendance_leave_list': research_attendance_leave_list,
        "research_name_list": research_name_list,
        "research_count_list_in_subject": research_count_list_in_subject,
        "research_count_list_in_organ": research_count_list_in_organ,
        "organ_name_list": organ_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)


def add_staff(request):
    form = StaffForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Staff'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            organ = form.cleaned_data.get('organ')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.staff.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_staff'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")

    return render(request, 'hod_template/add_staff_template.html', context)


def add_sugar(request):
    sugar_form = SugarForm(request.POST or None, request.FILES or None)
    context = {'form': sugar_form, 'page_title': 'Add Sugar'}

    if request.method == 'POST':
        if sugar_form.is_valid():
            real_person = sugar_form.cleaned_data.get('is_test')
            first_name = sugar_form.cleaned_data.get('first_name')
            last_name = sugar_form.cleaned_data.get('last_name')
            # address = sugar_form.cleaned_data.get('address')
            email = sugar_form.cleaned_data.get('email')
            gender = sugar_form.cleaned_data.get('gender')
            password = sugar_form.cleaned_data.get('password')
            organ = sugar_form.cleaned_data.get('organ')
            session = sugar_form.cleaned_data.get('session')
            # internal_company_phone_number = sugar_form.cleaned_data.get('internal_company_phone_number')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)

            # این فیلدها رو من اضافه کردم، اگه به مشکل خورد پاک بشه
            personal_number = sugar_form.cleaned_data.get('personal_number')
            access_level_number = sugar_form.cleaned_data.get('access_level_number')
            username = sugar_form.cleaned_data.get('username')
            wrong_passwords_number = sugar_form.cleaned_data.get('wrong_passwords_number')
            mobile_number = sugar_form.cleaned_data.get('mobile_number')
            home_phone_number = sugar_form.cleaned_data.get('home_phone_number')
            company_phone_number = sugar_form.cleaned_data.get('company_phone_number')
            internal_company_phone_number = sugar_form.cleaned_data.get('internal_company_phone_number')
            home_address = sugar_form.cleaned_data.get('home_address')
            company_address = sugar_form.cleaned_data.get('company_address')
            main_profile_image = sugar_form.cleaned_data.get('main_profile_image')
            company = sugar_form.cleaned_data.get('company')
            gregorian_datetime_create = sugar_form.cleaned_data.get('gregorian_datetime_create')
            gregorian_datetime_delete = sugar_form.cleaned_data.get('gregorian_datetime_delete')
            jalili_datetime_create = sugar_form.cleaned_data.get('jalili_datetime_create')
            jalili_datetime_delete = sugar_form.cleaned_data.get('jalili_datetime_delete')
            gregorian_birthday_datetime = sugar_form.cleaned_data.get('gregorian_birthday_datetime')
            jalili_birthday_datetime = sugar_form.cleaned_data.get('jalili_birthday_datetime')
            national_code = sugar_form.cleaned_data.get('national_code')
            birth_certificate_number = sugar_form.cleaned_data.get('birth_certificate_number')
            instagram_username = sugar_form.cleaned_data.get('instagram_username')
            telegram_id = sugar_form.cleaned_data.get('telegram_id')
            address = sugar_form.cleaned_data.get('address')
            house_location_x = sugar_form.cleaned_data.get('house_location_x')
            house_location_y = sugar_form.cleaned_data.get('house_location_y')
            company_location_x = sugar_form.cleaned_data.get('company_location_x')
            company_location_y = sugar_form.cleaned_data.get('company_location_y')
            residence_country = sugar_form.cleaned_data.get('residence_country')
            residence_city = sugar_form.cleaned_data.get('residence_city')
            birth_country = sugar_form.cleaned_data.get('birth_country')
            birth_city = sugar_form.cleaned_data.get('birth_city')
            family_numbers = sugar_form.cleaned_data.get('family_numbers')

            try:
                user = CustomUser.objects.create_user(
                    real_person=real_person, email=email, password=password, user_type=3, first_name=first_name,
                    last_name=last_name, profile_pic=passport_url,
                    personal_number=personal_number, access_level_number=access_level_number, username=username,
                    wrong_passwords_number=wrong_passwords_number, mobile_number=mobile_number,
                    home_phone_number=home_phone_number, company_phone_number=company_phone_number,
                    internal_company_phone_number=internal_company_phone_number, gender=gender,
                    home_address=home_address, company_address=company_address, main_profile_image=main_profile_image,
                    company=company,
                    gregorian_datetime_create=gregorian_datetime_create,
                    gregorian_datetime_delete=gregorian_datetime_delete, jalili_datetime_create=jalili_datetime_create,
                    jalili_datetime_delete=jalili_datetime_delete,
                    gregorian_birthday_datetime=gregorian_birthday_datetime,
                    jalili_birthday_datetime=jalili_birthday_datetime, national_code=national_code,
                    birth_certificate_number=birth_certificate_number, instagram_username=instagram_username,
                    telegram_id=telegram_id,
                    house_location_x=house_location_x, house_location_y=house_location_y,
                    company_location_x=company_location_x,
                    company_location_y=company_location_y, residence_country=residence_country,
                    residence_city=residence_city,
                    birth_country=birth_country, birth_city=birth_city, family_numbers=family_numbers,
                )
                user.gender = gender
                user.address = address
                user.sugar.session = session
                user.sugar.organ = organ
                user.save()
                user_email = str(request.user.email)
                # Specify the nested directory structure
                nested_directory = "main_app/static/upload/sugar/" + email

                # Create nested directories

                os.makedirs(nested_directory)

                messages.success(request, "Successfully Added")
                return redirect(reverse('add_sugar'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")

    return render(request, 'hod_template/add_sugar_template.html', context)


def add_kh(request):
    kh_form = KhForm(request.POST or None, request.FILES or None)
    context = {'form': kh_form, 'page_title': 'Add kh'}
    if request.method == 'POST':
        if kh_form.is_valid():
            first_name = kh_form.cleaned_data.get('first_name')
            last_name = kh_form.cleaned_data.get('last_name')
            address = kh_form.cleaned_data.get('address')
            email = kh_form.cleaned_data.get('email')
            gender = kh_form.cleaned_data.get('gender')
            password = kh_form.cleaned_data.get('password')
            organ = kh_form.cleaned_data.get('organ')
            session = kh_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=4, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.kh.session = session
                user.kh.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_kh'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_kh_template.html', context)


# old
"""
def add_person(request):
    person_form = PersonForm(request.POST or None, request.FILES or None)
    context = {'form': person_form, 'page_title': 'Add person'}

    if request.method == 'POST':
        if person_form.is_valid():
            first_name = person_form.cleaned_data.get('first_name')
            last_name = person_form.cleaned_data.get('last_name')
            address = person_form.cleaned_data.get('address')
            email = person_form.cleaned_data.get('email')
            gender = person_form.cleaned_data.get('gender')
            password = person_form.cleaned_data.get('password')
            organ = person_form.cleaned_data.get('organ')
            session = person_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=20, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.person.session = session
                user.person.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_person'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_person_template.html', context)
"""


# new
def add_person(request):
    person_form = PersonForm(request.POST or None, request.FILES or None)
    context = {'form': person_form, 'page_title': 'Add Person'}

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

    """
    USER_TYPE = (
        (20, "پرسون"),
        (5, "گروه توسعه صنایع شهد آذربایجان"),
        (3, "چغندر قند ارومیه"),
        (4, "قند خوی"),  # اضافه کردن نوع کاربر جدید
        (6, "قند پیرانشهر"),  # اضافه کردن نوع کاربر جدید
        (7, "'گلفام"),  # اضافه کردن نوع کاربر جدید
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
    """

    if request.method == 'POST':
        if person_form.is_valid():
            real_person = person_form.cleaned_data.get('real_person')
            first_name = person_form.cleaned_data.get('first_name')
            last_name = person_form.cleaned_data.get('last_name')
            # address = person_form.cleaned_data.get('address')
            email = person_form.cleaned_data.get('email')
            gender = person_form.cleaned_data.get('gender')
            password = person_form.cleaned_data.get('password')
            organ = person_form.cleaned_data.get('organ')
            session = person_form.cleaned_data.get('session')
            # internal_company_phone_number = person_form.cleaned_data.get('internal_company_phone_number')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            company = person_form.cleaned_data.get('company')
            user_type = person_form.cleaned_data.get('user_type')

            # این فیلدها رو من اضافه کردم، اگه به مشکل خورد پاک بشه
            post = person_form.cleaned_data.get('post')
            personal_number = person_form.cleaned_data.get('personal_number')
            access_level_number = person_form.cleaned_data.get('access_level_number')
            username = person_form.cleaned_data.get('username')
            wrong_passwords_number = person_form.cleaned_data.get('wrong_passwords_number')
            mobile_number = person_form.cleaned_data.get('mobile_number')
            home_phone_number = person_form.cleaned_data.get('home_phone_number')
            company_phone_number = person_form.cleaned_data.get('company_phone_number')
            internal_company_phone_number = person_form.cleaned_data.get('internal_company_phone_number')
            home_address = person_form.cleaned_data.get('home_address')
            company_address = person_form.cleaned_data.get('company_address')
            # main_profile_image = person_form.cleaned_data.get('main_profile_image')
            gregorian_datetime_create = person_form.cleaned_data.get('gregorian_datetime_create')
            gregorian_datetime_delete = person_form.cleaned_data.get('gregorian_datetime_delete')
            jalili_datetime_create = person_form.cleaned_data.get('jalili_datetime_create')
            jalili_datetime_delete = person_form.cleaned_data.get('jalili_datetime_delete')
            gregorian_birthday_datetime = person_form.cleaned_data.get('gregorian_birthday_datetime')
            jalili_birthday_datetime = person_form.cleaned_data.get('jalili_birthday_datetime')
            national_code = person_form.cleaned_data.get('national_code')
            birth_certificate_number = person_form.cleaned_data.get('birth_certificate_number')
            instagram_username = person_form.cleaned_data.get('instagram_username')
            telegram_id = person_form.cleaned_data.get('telegram_id')
            address = person_form.cleaned_data.get('address')
            # house_location_x = person_form.cleaned_data.get('house_location_x')
            # house_location_y = person_form.cleaned_data.get('house_location_y')
            # company_location_x = person_form.cleaned_data.get('company_location_x')
            # company_location_y = person_form.cleaned_data.get('company_location_y')
            residence_country = person_form.cleaned_data.get('residence_country')
            residence_city = person_form.cleaned_data.get('residence_city')
            birth_country = person_form.cleaned_data.get('birth_country')
            birth_city = person_form.cleaned_data.get('birth_city')
            family_numbers = person_form.cleaned_data.get('family_numbers')
            print(type(user_type))
            user_type = int(user_type)
            try:
                user = CustomUser.objects.create_user(
                    post=post, real_person=real_person, email=email, password=password, user_type=user_type,
                    first_name=first_name, last_name=last_name, profile_pic=passport_url,
                    personal_number=personal_number, access_level_number=access_level_number, username=username,
                    wrong_passwords_number=wrong_passwords_number, mobile_number=mobile_number,
                    home_phone_number=home_phone_number, company_phone_number=company_phone_number,
                    internal_company_phone_number=internal_company_phone_number,
                    home_address=home_address, company_address=company_address, company=company,
                    gregorian_datetime_create=gregorian_datetime_create,
                    gregorian_datetime_delete=gregorian_datetime_delete, jalili_datetime_create=jalili_datetime_create,
                    jalili_datetime_delete=jalili_datetime_delete,
                    gregorian_birthday_datetime=gregorian_birthday_datetime,
                    jalili_birthday_datetime=jalili_birthday_datetime, national_code=national_code,
                    birth_certificate_number=birth_certificate_number, instagram_username=instagram_username,
                    telegram_id=telegram_id, residence_country=residence_country,
                    residence_city=residence_city, birth_country=birth_country, birth_city=birth_city,
                    family_numbers=family_numbers
                )

                this_company_string = ''

                for i in USER_TYPE:
                    if i[0] == user_type:
                        this_company_string = i[1]

                s = this_company_string.lower()
                s1 = "user." + s + ".session = session"
                s2 = "user." + s + ".organ = organ"
                exec(s1)
                exec(s2)

                user.save()

                user_email = str(request.user.email)

                # Specify the nested directory structure
                try:
                    nested_directory = "main_app//static//upload//{0}//{1}".format(this_company_string, email)
                    print(nested_directory)
                    # Create nested directories
                    os.makedirs(nested_directory)
                except:
                    pass
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_person'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")

    return render(request, 'hod_template/add_person_template.html', context)


"""
# new
def add_person(request):
    person_form = PersonForm(request.POST or None, request.FILES or None)
    context = {'form': person_form, 'page_title': 'Add Person'}

    if request.method == 'POST':
        if person_form.is_valid():
            real_person = person_form.cleaned_data.get('real_person')
            first_name = person_form.cleaned_data.get('first_name')
            last_name = person_form.cleaned_data.get('last_name')
            # address = person_form.cleaned_data.get('address')
            email = person_form.cleaned_data.get('email')
            gender = person_form.cleaned_data.get('gender')
            password = person_form.cleaned_data.get('password')
            organ = person_form.cleaned_data.get('organ')
            session = person_form.cleaned_data.get('session')
            # internal_company_phone_number = person_form.cleaned_data.get('internal_company_phone_number')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            company = person_form.cleaned_data.get('company')
            user_type = person_form.cleaned_data.get('user_type')

            # این فیلدها رو من اضافه کردم، اگه به مشکل خورد پاک بشه
            personal_number = person_form.cleaned_data.get('personal_number')
            access_level_number = person_form.cleaned_data.get('access_level_number')
            username = person_form.cleaned_data.get('username')
            wrong_passwords_number = person_form.cleaned_data.get('wrong_passwords_number')
            mobile_number = person_form.cleaned_data.get('mobile_number')
            home_phone_number = person_form.cleaned_data.get('home_phone_number')
            company_phone_number = person_form.cleaned_data.get('company_phone_number')
            internal_company_phone_number = person_form.cleaned_data.get('internal_company_phone_number')
            home_address = person_form.cleaned_data.get('home_address')
            company_address = person_form.cleaned_data.get('company_address')
            # main_profile_image = person_form.cleaned_data.get('main_profile_image')
            gregorian_datetime_create = person_form.cleaned_data.get('gregorian_datetime_create')
            gregorian_datetime_delete = person_form.cleaned_data.get('gregorian_datetime_delete')
            jalili_datetime_create = person_form.cleaned_data.get('jalili_datetime_create')
            jalili_datetime_delete = person_form.cleaned_data.get('jalili_datetime_delete')
            gregorian_birthday_datetime = person_form.cleaned_data.get('gregorian_birthday_datetime')
            jalili_birthday_datetime = person_form.cleaned_data.get('jalili_birthday_datetime')
            national_code = person_form.cleaned_data.get('national_code')
            birth_certificate_number = person_form.cleaned_data.get('birth_certificate_number')
            instagram_username = person_form.cleaned_data.get('instagram_username')
            telegram_id = person_form.cleaned_data.get('telegram_id')
            address = person_form.cleaned_data.get('address')
            # house_location_x = person_form.cleaned_data.get('house_location_x')
            # house_location_y = person_form.cleaned_data.get('house_location_y')
            # company_location_x = person_form.cleaned_data.get('company_location_x')
            # company_location_y = person_form.cleaned_data.get('company_location_y')
            residence_country = person_form.cleaned_data.get('residence_country')
            residence_city = person_form.cleaned_data.get('residence_city')
            birth_country = person_form.cleaned_data.get('birth_country')
            birth_city = person_form.cleaned_data.get('birth_city')
            family_numbers = person_form.cleaned_data.get('family_numbers')
            try:
                user = CustomUser.objects.create_user(
                    real_person=real_person, email=email, password=password, user_type=user_type, first_name=first_name,
                    last_name=last_name, profile_pic=passport_url,
                    personal_number=personal_number, access_level_number=access_level_number, username=username,
                    wrong_passwords_number=wrong_passwords_number, mobile_number=mobile_number,
                    home_phone_number=home_phone_number, company_phone_number=company_phone_number,
                    internal_company_phone_number=internal_company_phone_number,
                    home_address=home_address, company_address=company_address, company=company,
                    gregorian_datetime_create=gregorian_datetime_create,
                    gregorian_datetime_delete=gregorian_datetime_delete, jalili_datetime_create=jalili_datetime_create,
                    jalili_datetime_delete=jalili_datetime_delete,
                    gregorian_birthday_datetime=gregorian_birthday_datetime,
                    jalili_birthday_datetime=jalili_birthday_datetime, national_code=national_code,
                    birth_certificate_number=birth_certificate_number, instagram_username=instagram_username,
                    telegram_id=telegram_id, residence_country=residence_country,
                    residence_city=residence_city, birth_country=birth_country, birth_city=birth_city,
                    family_numbers=family_numbers
                )
                user.gender = gender
                user.address = address
                user.holding.session = session
                user.holding.organ = organ
                user.save()
                user_email = str(request.user.email)
                # Specify the nested directory structure
                nested_directory = "main_app/static/upload/person/" + email

                # Create nested directories

                os.makedirs(nested_directory)
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_person'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")

    return render(request, 'hod_template/add_person_template.html', context)
"""


def add_holding(request):
    holding_form = HoldingForm(request.POST or None, request.FILES or None)
    context = {'form': holding_form, 'page_title': 'Add holding'}

    if request.method == 'POST':
        if holding_form.is_valid():
            first_name = holding_form.cleaned_data.get('first_name')
            last_name = holding_form.cleaned_data.get('last_name')
            address = holding_form.cleaned_data.get('address')
            email = holding_form.cleaned_data.get('email')
            gender = holding_form.cleaned_data.get('gender')
            password = holding_form.cleaned_data.get('password')
            organ = holding_form.cleaned_data.get('organ')
            session = holding_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=5, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)

                user.gender = gender
                user.address = address
                user.holding.session = session
                user.holding.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_holding'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_holding_template.html', context)


def add_piran(request):
    piran_form = PiranForm(request.POST or None, request.FILES or None)
    context = {'form': piran_form, 'page_title': 'Add piran'}
    if request.method == 'POST':
        if piran_form.is_valid():
            first_name = piran_form.cleaned_data.get('first_name')
            last_name = piran_form.cleaned_data.get('last_name')
            address = piran_form.cleaned_data.get('address')
            email = piran_form.cleaned_data.get('email')
            gender = piran_form.cleaned_data.get('gender')
            password = piran_form.cleaned_data.get('password')
            organ = piran_form.cleaned_data.get('organ')
            session = piran_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=6, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.piran.session = session
                user.piran.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_piran'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_piran_template.html', context)


def add_tomato(request):
    tomato_form = TomatoForm(request.POST or None, request.FILES or None)
    context = {'form': tomato_form, 'page_title': 'Add tomato'}
    if request.method == 'POST':
        if tomato_form.is_valid():
            first_name = tomato_form.cleaned_data.get('first_name')
            last_name = tomato_form.cleaned_data.get('last_name')
            address = tomato_form.cleaned_data.get('address')
            email = tomato_form.cleaned_data.get('email')
            gender = tomato_form.cleaned_data.get('gender')
            password = tomato_form.cleaned_data.get('password')
            organ = tomato_form.cleaned_data.get('organ')
            session = tomato_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=7, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.tomato.session = session
                user.tomato.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_tomato'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_tomato_template.html', context)


def add_taraghi(request):
    taraghi_form = TaraghiForm(request.POST or None, request.FILES or None)
    context = {'form': taraghi_form, 'page_title': 'Add taraghi'}
    if request.method == 'POST':
        if taraghi_form.is_valid():
            first_name = taraghi_form.cleaned_data.get('first_name')
            last_name = taraghi_form.cleaned_data.get('last_name')
            address = taraghi_form.cleaned_data.get('address')
            email = taraghi_form.cleaned_data.get('email')
            gender = taraghi_form.cleaned_data.get('gender')
            password = taraghi_form.cleaned_data.get('password')
            organ = taraghi_form.cleaned_data.get('organ')
            session = taraghi_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=8, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.taraghi.session = session
                user.taraghi.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_taraghi'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_taraghi_template.html', context)


def add_tootia(request):
    tootia_form = TootiaForm(request.POST or None, request.FILES or None)
    context = {'form': tootia_form, 'page_title': 'Add tootia'}
    if request.method == 'POST':
        if tootia_form.is_valid():
            first_name = tootia_form.cleaned_data.get('first_name')
            last_name = tootia_form.cleaned_data.get('last_name')
            address = tootia_form.cleaned_data.get('address')
            email = tootia_form.cleaned_data.get('email')
            gender = tootia_form.cleaned_data.get('gender')
            password = tootia_form.cleaned_data.get('password')
            organ = tootia_form.cleaned_data.get('organ')
            session = tootia_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=9, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.tootia.session = session
                user.tootia.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_tootia'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_tootia_template.html', context)


def add_drug(request):
    drug_form = DrugForm(request.POST or None, request.FILES or None)
    context = {'form': drug_form, 'page_title': 'Add drug'}
    if request.method == 'POST':
        if drug_form.is_valid():
            first_name = drug_form.cleaned_data.get('first_name')
            last_name = drug_form.cleaned_data.get('last_name')
            address = drug_form.cleaned_data.get('address')
            email = drug_form.cleaned_data.get('email')
            gender = drug_form.cleaned_data.get('gender')
            password = drug_form.cleaned_data.get('password')
            organ = drug_form.cleaned_data.get('organ')
            session = drug_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=10, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.drug.session = session
                user.drug.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_drug'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_drug_template.html', context)


def add_gen(request):
    gen_form = GenForm(request.POST or None, request.FILES or None)
    context = {'form': gen_form, 'page_title': 'Add gen'}
    if request.method == 'POST':
        if gen_form.is_valid():
            first_name = gen_form.cleaned_data.get('first_name')
            last_name = gen_form.cleaned_data.get('last_name')
            address = gen_form.cleaned_data.get('address')
            email = gen_form.cleaned_data.get('email')
            gender = gen_form.cleaned_data.get('gender')
            password = gen_form.cleaned_data.get('password')
            organ = gen_form.cleaned_data.get('organ')
            session = gen_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=11, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.gen.session = session
                user.gen.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_gen'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_gen_template.html', context)


def add_iron(request):
    iron_form = IronForm(request.POST or None, request.FILES or None)
    context = {'form': iron_form, 'page_title': 'Add iron'}
    if request.method == 'POST':
        if iron_form.is_valid():
            first_name = iron_form.cleaned_data.get('first_name')
            last_name = iron_form.cleaned_data.get('last_name')
            address = iron_form.cleaned_data.get('address')
            email = iron_form.cleaned_data.get('email')
            gender = iron_form.cleaned_data.get('gender')
            password = iron_form.cleaned_data.get('password')
            organ = iron_form.cleaned_data.get('organ')
            session = iron_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=12, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.iron.session = session
                user.iron.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_iron'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_iron_template.html', context)


def add_ptro(request):
    ptro_form = PtroForm(request.POST or None, request.FILES or None)
    context = {'form': ptro_form, 'page_title': 'Add ptro'}
    if request.method == 'POST':
        if ptro_form.is_valid():
            first_name = ptro_form.cleaned_data.get('first_name')
            last_name = ptro_form.cleaned_data.get('last_name')
            address = ptro_form.cleaned_data.get('address')
            email = ptro_form.cleaned_data.get('email')
            gender = ptro_form.cleaned_data.get('gender')
            password = ptro_form.cleaned_data.get('password')
            organ = ptro_form.cleaned_data.get('organ')
            session = ptro_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=13, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.ptro.session = session
                user.ptro.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_ptro'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_ptro_template.html', context)


def add_agriculture(request):
    agriculture_form = AgricultureForm(request.POST or None, request.FILES or None)
    context = {'form': agriculture_form, 'page_title': 'Add agriculture'}
    if request.method == 'POST':
        if agriculture_form.is_valid():
            first_name = agriculture_form.cleaned_data.get('first_name')
            last_name = agriculture_form.cleaned_data.get('last_name')
            address = agriculture_form.cleaned_data.get('address')
            email = agriculture_form.cleaned_data.get('email')
            gender = agriculture_form.cleaned_data.get('gender')
            password = agriculture_form.cleaned_data.get('password')
            organ = agriculture_form.cleaned_data.get('organ')
            session = agriculture_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=14, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.agriculture.session = session
                user.agriculture.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_agriculture'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_agriculture_template.html', context)


def add_research(request):
    research_form = ResearchForm(request.POST or None, request.FILES or None)
    context = {'form': research_form, 'page_title': 'Add research'}
    if request.method == 'POST':
        if research_form.is_valid():
            first_name = research_form.cleaned_data.get('first_name')
            last_name = research_form.cleaned_data.get('last_name')
            address = research_form.cleaned_data.get('address')
            email = research_form.cleaned_data.get('email')
            gender = research_form.cleaned_data.get('gender')
            password = research_form.cleaned_data.get('password')
            organ = research_form.cleaned_data.get('organ')
            session = research_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=15, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.research.session = session
                user.research.organ = organ
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_research'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_research_template.html', context)


def add_organ(request):
    form = OrganForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Area of activity'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                organ = Organ()
                organ.name = name
                organ.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_organ'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'hod_template/add_organ_template.html', context)


def add_subject(request):
    form = SubjectForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            organ = form.cleaned_data.get('organ')
            staff = form.cleaned_data.get('staff')
            try:
                subject = Subject()
                subject.name = name
                subject.staff = staff
                subject.organ = organ
                subject.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_subject'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'hod_template/add_subject_template.html', context)


def manage_staff(request):
    allStaff = CustomUser.objects.filter(user_type=2)
    context = {
        'allStaff': allStaff,
        'page_title': 'Manage Staff'
    }
    return render(request, "hod_template/manage_staff.html", context)


def manage_sugar(request):
    sugars = CustomUser.objects.filter(user_type=3)
    context = {
        'sugars': sugars,
        'page_title': 'Manage Sugars'
    }
    return render(request, "hod_template/manage_sugar.html", context)


def manage_kh(request):
    khs = CustomUser.objects.filter(user_type=4)

    context = {
        'khs': khs,
        'page_title': 'Manage khs'
    }
    return render(request, "hod_template/manage_kh.html", context)


def manage_person(request):
    persons = CustomUser.objects.all()

    context = {
        'persons': persons,
        'page_title': 'Manage persons'
    }

    return render(request, "hod_template/manage_person.html", context)


def manage_holding(request):
    holdings = CustomUser.objects.filter(user_type=5)

    context = {
        'holdings': holdings,
        'page_title': 'Manage holdings'
    }
    return render(request, "hod_template/manage_holding.html", context)


def manage_piran(request):
    pirans = CustomUser.objects.filter(user_type=6)
    context = {
        'pirans': pirans,
        'page_title': 'Manage pirans'
    }
    return render(request, "hod_template/manage_piran.html", context)


def manage_tomato(request):
    tomatos = CustomUser.objects.filter(user_type=7)
    context = {
        'tomatos': tomatos,
        'page_title': 'Manage tomatos'
    }
    return render(request, "hod_template/manage_tomato.html", context)


def manage_taraghi(request):
    taraghis = CustomUser.objects.filter(user_type=8)
    context = {
        'taraghis': taraghis,
        'page_title': 'Manage taraghis'
    }
    return render(request, "hod_template/manage_taraghi.html", context)


def manage_tootia(request):
    tootias = CustomUser.objects.filter(user_type=9)
    context = {
        'tootias': tootias,
        'page_title': 'Manage tootias'
    }
    return render(request, "hod_template/manage_tootia.html", context)


def manage_drug(request):
    drugs = CustomUser.objects.filter(user_type=10)
    context = {
        'drugs': drugs,
        'page_title': 'Manage drugs'
    }
    return render(request, "hod_template/manage_drug.html", context)


def manage_gen(request):
    gens = CustomUser.objects.filter(user_type=11)

    context = {
        'gens': gens,
        'page_title': 'Manage gens'
    }
    return render(request, "hod_template/manage_gen.html", context)


def manage_iron(request):
    irons = CustomUser.objects.filter(user_type=12)
    context = {
        'irons': irons,
        'page_title': 'Manage irons'
    }
    return render(request, "hod_template/manage_iron.html", context)


def manage_ptro(request):
    ptros = CustomUser.objects.filter(user_type=13)
    context = {
        'ptros': ptros,
        'page_title': 'Manage ptros'
    }
    return render(request, "hod_template/manage_ptro.html", context)


def manage_agriculture(request):
    agricultures = CustomUser.objects.filter(user_type=14)
    context = {
        'agricultures': agricultures,
        'page_title': 'Manage agricultures'
    }
    return render(request, "hod_template/manage_agriculture.html", context)


def manage_research(request):
    researchs = CustomUser.objects.filter(user_type=15)
    context = {
        'researchs': researchs,
        'page_title': 'Manage researchs'
    }
    return render(request, "hod_template/manage_research.html", context)


def manage_organ(request):
    organs = Organ.objects.all()
    context = {
        'organs': organs,
        'page_title': 'Manage Organs'
    }
    return render(request, "hod_template/manage_organ.html", context)


def manage_subject(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
        'page_title': 'Manage Subjects'
    }
    return render(request, "hod_template/manage_subject.html", context)


def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    form = StaffForm(request.POST or None, instance=staff)
    context = {
        'form': form,
        'staff_id': staff_id,
        'page_title': 'Edit Staff'
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
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=staff.admin.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                staff.organ = organ
                user.save()
                staff.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_staff', args=[staff_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fil form properly")
    else:
        user = CustomUser.objects.get(id=staff_id)
        staff = Staff.objects.get(id=user.id)
        return render(request, "hod_template/edit_staff_template.html", context)


def edit_sugar(request, sugar_id):
    sugar = get_object_or_404(Sugar, id=sugar_id)
    form = SugarForm(request.POST or None, instance=sugar)
    context = {
        'form': form,
        'sugar_id': sugar_id,
        'page_title': 'Edit Sugar'
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
                user = CustomUser.objects.get(id=sugar.admin.id)
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
                sugar.session = session
                user.gender = gender
                user.address = address
                sugar.organ = organ
                user.save()
                sugar.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_sugar', args=[sugar_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_sugar_template.html", context)


def edit_kh(request, kh_id):
    kh = get_object_or_404(Kh, id=kh_id)
    form = KhForm(request.POST or None, instance=kh)
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
                return redirect(reverse('edit_kh', args=[kh_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_kh_template.html", context)


def edit_person(request, person_id):
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
    # نیاز به دیباگ داره این متد درست کار نمیکنه
    # نیاز به دیباگ داره این متد درست کار نمیکنه
    # نیاز به دیباگ داره این متد درست کار نمیکنه
    # نیاز به دیباگ داره این متد درست کار نمیکنه
    user_type_first_item = int(CustomUser.objects.filter(id=person_id).values_list('user_type', flat=True)[0])
    this_company = ""
    for i in USER_TYPE:
        if i[0] == user_type_first_item:
            this_company = str(i[1])

    module_name = "models"
    class_name = this_company
    ModelClass = ""
    try:
        ModelClass = apps.get_model('main_app', this_company)
        print(type(ModelClass))
        # objects = ModelClass.objects.all().values()
        # print(objects)
    except:
        print("not successfull")

    user1 = CustomUser.objects.get(id=person_id)

    rel2 = "drug"
    # s = exec(str(user1) + '.' + str(rel2))
    this_company = this_company[0].lower() + this_company[1:]

    related_name = this_company
    author = CustomUser.objects.get(id=person_id)
    profile = getattr(author, related_name)
    """
    this_company = this_company[0].lower() + this_company[1:]
    customuser_object = CustomUser.objects.get(id=person_id)
    this_instance = exec(str(customuser_object) + "." + str(this_company))
    this_instance = CustomUser.objects.filter(this_company__admin=customuser_object)
    # this_instance = customuser_object.this_company.all()
    s = "main_app.models." + this_company
    this_company = eval(this_company)
    this_id = str(
        exec(str(customuser_object) + "." + this_company + "_set.all().first().values_list('id',flat=True)[0]"))
    """
    this_id = profile.id
    # person=ModelClass.objects.get(email=profile.admin.email)
    # print(person)
    person = get_object_or_404(ModelClass, id=this_id)
    form = PersonForm(request.POST or None, instance=person)
    context = {
        'form': form,
        'person_id': this_id,
        'page_title': 'Edit Person'
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
            real_person = form.cleaned_data.get('real_person')
            access_level_number = form.cleaned_data.get('access_level_number')
            device_panel = form.cleaned_data.get('device_panel')
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            print(device_panel)
            try:
                user = CustomUser.objects.get(id=person.admin.id)
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
                user.session = session
                user.gender = gender
                user.address = address
                user.organ = organ
                user.real_person = real_person
                user.access_level_number = access_level_number
                user.device_panel = device_panel

                user.save()
                # person.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_person', args=[person_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, form.errors)
            messages.error(request, "Please Fill Form Properly!")
            return redirect(reverse('edit_person', args=[person_id]))
    else:
        return render(request, "hod_template/edit_person_template.html", context)


def edit_holding(request, holding_id):
    holding = get_object_or_404(Holding, id=holding_id)
    form = HoldingForm(request.POST or None, instance=holding)
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
                return redirect(reverse('edit_holding', args=[holding_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_holding_template.html", context)


def edit_piran(request, piran_id):
    piran = get_object_or_404(Piran, id=piran_id)
    form = PiranForm(request.POST or None, instance=piran)
    context = {
        'form': form,
        'piran_id': piran_id,
        'page_title': 'Edit Piran'
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
                user = CustomUser.objects.get(id=piran.admin.id)
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
                piran.session = session
                user.gender = gender
                user.address = address
                piran.organ = organ
                user.save()
                piran.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_piran', args=[piran_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_piran_template.html", context)


def edit_tomato(request, tomato_id):
    tomato = get_object_or_404(Tomato, id=tomato_id)
    form = TomatoForm(request.POST or None, instance=tomato)
    context = {
        'form': form,
        'tomato_id': tomato_id,
        'page_title': 'Edit tomato'
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
                user = CustomUser.objects.get(id=tomato.admin.id)
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
                tomato.session = session
                user.gender = gender
                user.address = address
                tomato.organ = organ
                user.save()
                tomato.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_tomato', args=[tomato_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_tomato_template.html", context)


def edit_taraghi(request, taraghi_id):
    taraghi = get_object_or_404(Taraghi, id=taraghi_id)
    form = TaraghiForm(request.POST or None, instance=taraghi)
    context = {
        'form': form,
        'taraghi_id': taraghi_id,
        'page_title': 'Edit Taraghi'
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
                user = CustomUser.objects.get(id=taraghi.admin.id)
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
                taraghi.session = session
                user.gender = gender
                user.address = address
                taraghi.organ = organ
                user.save()
                taraghi.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_taraghi', args=[taraghi_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_taraghi_template.html", context)


def edit_tootia(request, tootia_id):
    tootia = get_object_or_404(Tootia, id=tootia_id)
    form = TootiaForm(request.POST or None, instance=tootia)
    context = {
        'form': form,
        'tootia_id': tootia_id,
        'page_title': 'Edit Tootia'
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
                user = CustomUser.objects.get(id=tootia.admin.id)
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
                tootia.session = session
                user.gender = gender
                user.address = address
                tootia.organ = organ
                user.save()
                tootia.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_tootia', args=[tootia_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_tootia_template.html", context)


def edit_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    form = DrugForm(request.POST or None, instance=drug)
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
                return redirect(reverse('edit_drug', args=[drug_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_drug_template.html", context)


def edit_gen(request, gen_id):
    gen = get_object_or_404(Gen, id=gen_id)
    form = GenForm(request.POST or None, instance=gen)
    context = {
        'form': form,
        'gen_id': gen_id,
        'page_title': 'Edit Gen'
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
                user = CustomUser.objects.get(id=gen.admin.id)
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
                gen.session = session
                user.gender = gender
                user.address = address
                gen.organ = organ
                user.save()
                gen.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_gen', args=[gen_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_gen_template.html", context)


def edit_iron(request, iron_id):
    iron = get_object_or_404(Iron, id=iron_id)
    form = IronForm(request.POST or None, instance=iron)
    context = {
        'form': form,
        'iron_id': iron_id,
        'page_title': 'Edit Iron'
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
                user = CustomUser.objects.get(id=iron.admin.id)
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
                iron.session = session
                user.gender = gender
                user.address = address
                iron.organ = organ
                user.save()
                iron.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_iron', args=[iron_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_iron_template.html", context)


def edit_ptro(request, ptro_id):
    ptro = get_object_or_404(Ptro, id=ptro_id)
    form = PtroForm(request.POST or None, instance=ptro)
    context = {
        'form': form,
        'ptro_id': ptro_id,
        'page_title': 'Edit Ptro'
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
                user = CustomUser.objects.get(id=ptro.admin.id)
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
                ptro.session = session
                user.gender = gender
                user.address = address
                ptro.organ = organ
                user.save()
                ptro.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_ptro', args=[ptro_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_ptro_template.html", context)


def edit_agriculture(request, agriculture_id):
    agriculture = get_object_or_404(Agriculture, id=agriculture_id)
    form = AgricultureForm(request.POST or None, instance=agriculture)
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
                return redirect(reverse('edit_agriculture', args=[agriculture_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_agriculture_template.html", context)


def edit_research(request, research_id):
    research = get_object_or_404(Research, id=research_id)
    form = ResearchForm(request.POST or None, instance=research)
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
                return redirect(reverse('edit_research', args=[research_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_research_template.html", context)


def edit_organ(request, organ_id):
    instance = get_object_or_404(Organ, id=organ_id)
    form = OrganForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'organ_id': organ_id,
        'page_title': 'Edit Organ'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                organ = Organ.objects.get(id=organ_id)
                organ.name = name
                organ.save()
                messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'hod_template/edit_organ_template.html', context)


def edit_subject(request, subject_id):
    instance = get_object_or_404(Subject, id=subject_id)
    form = SubjectForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'subject_id': subject_id,
        'page_title': 'Edit Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            organ = form.cleaned_data.get('organ')
            staff = form.cleaned_data.get('staff')
            try:
                subject = Subject.objects.get(id=subject_id)
                subject.name = name
                subject.staff = staff
                subject.organ = organ
                subject.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_subject', args=[subject_id]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'hod_template/edit_subject_template.html', context)


def add_session(request):
    form = SessionForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Created")
                return redirect(reverse('add_session'))
            except Exception as e:
                messages.error(request, 'Could Not Add ' + str(e))
        else:
            messages.error(request, 'Fill Form Properly ')
    return render(request, "hod_template/add_session_template.html", context)


def manage_session(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions, 'page_title': 'Manage Sessions'}
    return render(request, "hod_template/manage_session.html", context)


def edit_session(request, session_id):
    instance = get_object_or_404(Session, id=session_id)
    form = SessionForm(request.POST or None, instance=instance)
    context = {'form': form, 'session_id': session_id,
               'page_title': 'Edit Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Updated")
                return redirect(reverse('edit_session', args=[session_id]))
            except Exception as e:
                messages.error(
                    request, "Session Could Not Be Updated " + str(e))
                return render(request, "hod_template/edit_session_template.html", context)
        else:
            messages.error(request, "Invalid Form Submitted ")
            return render(request, "hod_template/edit_session_template.html", context)

    else:
        return render(request, "hod_template/edit_session_template.html", context)


@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


@csrf_exempt
def sugar_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackSugar.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Sugar Feedback Messages'
        }
        return render(request, 'hod_template/sugar_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackSugar, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def kh_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackKh.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Kh personal Messages'
        }
        return render(request, 'hod_template/kh_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackKh, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def person_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackPerson.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Person personal Messages'
        }
        return render(request, 'hod_template/person_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackPerson, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def holding_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackHolding.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Holding personal Messages'
        }
        return render(request, 'hod_template/holding_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackHolding, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def piran_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackPiran.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Piran personal Messages'
        }
        return render(request, 'hod_template/piran_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackPiran, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def tomato_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackTomato.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'tomato personal Messages'
        }
        return render(request, 'hod_template/tomato_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackTomato, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def taraghi_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackTaraghi.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Taraghi personal Messages'
        }
        return render(request, 'hod_template/taraghi_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackTaraghi, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def tootia_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackTootia.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Tootia personal Messages'
        }
        return render(request, 'hod_template/tootia_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackTootia, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def drug_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackDrug.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Drug personal Messages'
        }
        return render(request, 'hod_template/drug_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackDrug, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def gen_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackGen.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Gen personal Messages'
        }
        return render(request, 'hod_template/gen_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackGen, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def iron_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackIron.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Iron personal Messages'
        }
        return render(request, 'hod_template/iron_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackIron, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def ptro_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackPtro.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Ptro personal Messages'
        }
        return render(request, 'hod_template/ptro_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackPtro, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def agriculture_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackAgriculture.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Agriculture personal Messages'
        }
        return render(request, 'hod_template/agriculture_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackAgriculture, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def research_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackResearch.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Research personal Messages'
        }
        return render(request, 'hod_template/research_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackResearch, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def staff_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackStaff.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Staff Feedback Messages'
        }
        return render(request, 'hod_template/staff_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStaff, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def view_staff_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportStaff.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Staff'
        }
        return render(request, "hod_template/staff_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStaff, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_sugar_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportSugar.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request From Sugars memeber'
        }
        return render(request, "hod_template/sugar_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportSugar, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_kh_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportKh.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From khoy personal'
        }
        return render(request, "hod_template/kh_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportKh, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_person_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportPerson.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From Persons memeber'
        }
        return render(request, "hod_template/person_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportPerson, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_holding_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportHolding.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From Holdings memeber'
        }
        return render(request, "hod_template/holding_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportHolding, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_piran_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportPiran.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From Pirans memeber'
        }
        return render(request, "hod_template/piran_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportPiran, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_tomato_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportTomato.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From Tomatos memeber'
        }
        return render(request, "hod_template/tomato_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportTomato, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_taraghi_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportTaraghi.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From Taraghis memeber'
        }
        return render(request, "hod_template/taraghi_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportTaraghi, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_tootia_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportTootia.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From Tootias memeber'
        }
        return render(request, "hod_template/tootia_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportTootia, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_drug_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportDrug.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From Drugs memeber'
        }
        return render(request, "hod_template/drug_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportDrug, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_gen_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportGen.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From Gens memeber'
        }
        return render(request, "hod_template/gen_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportGen, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_iron_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportIron.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From Irons memeber'
        }
        return render(request, "hod_template/iron_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportIron, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


def admin_view_attendance(request):
    subjects = Subject.objects.all()
    sessions = Session.objects.all()
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'View Attendance'
    }

    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def view_ptro_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportPtro.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From Ptros memeber'
        }
        return render(request, "hod_template/ptro_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportPtro, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_agriculture_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportAgriculture.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From Agricultures memeber'
        }
        return render(request, "hod_template/agriculture_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportAgriculture, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_research_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportResearch.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'request  From Researchs memeber'
        }
        return render(request, "hod_template/research_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportResearch, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def get_admin_attendance(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        attendance = get_object_or_404(
            Attendance, id=attendance_date_id, session=session)
        attendance_reports = AttendanceReport.objects.filter(
            attendance=attendance)
        json_data = []
        for report in attendance_reports:
            data = {
                "status": str(report.status),
                "name": str(report.sugar),
                "namekh": str(report.kh),
                "nameperson": str(report.person),
                "nameholding": str(report.holding),
                "namepiran": str(report.piran),
                "nametomato": str(report.tomato),
                "nametaraghi": str(report.taraghi),
                "nametootia": str(report.tootia),
                "namedrug": str(report.drug),
                "namegen": str(report.gen),
                "nameiron": str(report.iron),
                "nameptro": str(report.ptro),
                "nameagriculture": str(report.agriculture),
                "nameresearch": str(report.research),

            }
            json_data.append(data)
        return JsonResponse(json.dumps(json_data), safe=False)
    except Exception as e:
        return None


def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "hod_template/admin_view_profile.html", context)


def admin_notify_staff(request):
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To Staff",
        'allStaff': staff
    }
    return render(request, "hod_template/staff_notification.html", context)


def admin_notify_sugar(request):
    sugar = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': "Send Notifications To Sugars",
        'sugars': sugar
    }
    return render(request, "hod_template/sugar_notification.html", context)


def admin_notify_kh(request):
    kh = CustomUser.objects.filter(user_type=4)
    context = {
        'page_title': "Send Notifications To Khs",
        'khs': kh
    }
    return render(request, "hod_template/kh_notification.html", context)


def admin_notify_person(request):
    person = CustomUser.objects.filter(user_type=5)
    context = {
        'page_title': "Send Notifications To Persons",
        'persons': person
    }
    return render(request, "hod_template/person_notification.html", context)


def admin_notify_holding(request):
    holding = CustomUser.objects.filter(user_type=5)
    context = {
        'page_title': "Send Notifications To Holdings",
        'holdings': holding
    }
    return render(request, "hod_template/holding_notification.html", context)


def admin_notify_piran(request):
    piran = CustomUser.objects.filter(user_type=6)
    context = {
        'page_title': "Send Notifications To Pirans",
        'pirans': piran
    }
    return render(request, "hod_template/piran_notification.html", context)


def admin_notify_tomato(request):
    tomato = CustomUser.objects.filter(user_type=7)
    context = {
        'page_title': "Send Notifications To Tomatos",
        'tomatos': tomato
    }
    return render(request, "hod_template/tomato_notification.html", context)


def admin_notify_taraghi(request):
    taraghi = CustomUser.objects.filter(user_type=8)
    context = {
        'page_title': "Send Notifications To Taraghis",
        'taraghis': taraghi
    }
    return render(request, "hod_template/taraghi_notification.html", context)


def admin_notify_tootia(request):
    tootia = CustomUser.objects.filter(user_type=9)
    context = {
        'page_title': "Send Notifications To Tootias",
        'tootias': tootia
    }
    return render(request, "hod_template/tootia_notification.html", context)


def admin_notify_drug(request):
    drug = CustomUser.objects.filter(user_type=10)
    context = {
        'page_title': "Send Notifications To Drugs",
        'drugs': drug
    }
    return render(request, "hod_template/drug_notification.html", context)


def admin_notify_gen(request):
    gen = CustomUser.objects.filter(user_type=11)
    context = {
        'page_title': "Send Notifications To Gens",
        'gens': gen
    }
    return render(request, "hod_template/gen_notification.html", context)


def admin_notify_iron(request):
    iron = CustomUser.objects.filter(user_type=12)
    context = {
        'page_title': "Send Notifications To Irons",
        'irons': iron
    }
    return render(request, "hod_template/iron_notification.html", context)


def admin_notify_ptro(request):
    ptro = CustomUser.objects.filter(user_type=13)
    context = {
        'page_title': "Send Notifications To Ptros",
        'ptros': ptro
    }
    return render(request, "hod_template/ptro_notification.html", context)


def admin_notify_agriculture(request):
    agriculture = CustomUser.objects.filter(user_type=14)
    context = {
        'page_title': "Send Notifications To Agricultures",
        'agricultures': agriculture
    }
    return render(request, "hod_template/agriculture_notification.html", context)


def admin_notify_research(request):
    research = CustomUser.objects.filter(user_type=15)
    context = {
        'page_title': "Send Notifications To Researchs",
        'researchs': research
    }
    return render(request, "hod_template/research_notification.html", context)


@csrf_exempt
def send_sugar_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    sugar = get_object_or_404(Sugar, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Sugar Management System",
                'body': message,
                'click_action': reverse('sugar_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': sugar.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationSugar(sugar=sugar, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_kh_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    kh = get_object_or_404(Kh, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Kh Management System",
                'body': message,
                'click_action': reverse('kh_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': kh.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationKh(kh=kh, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_person_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    person = get_object_or_404(Person, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Person Management System",
                'body': message,
                'click_action': reverse('person_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': person.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationPerson(person=person, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_holding_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    holding = get_object_or_404(Holding, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Holding Management System",
                'body': message,
                'click_action': reverse('holding_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': holding.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationHolding(holding=holding, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_piran_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    piran = get_object_or_404(Piran, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "piran shahr Management System",
                'body': message,
                'click_action': reverse('piran_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': piran.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationPiran(piran=piran, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_tomato_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    tomato = get_object_or_404(Tomato, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "tomato shahr Management System",
                'body': message,
                'click_action': reverse('tomato_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': tomato.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationTomato(tomato=tomato, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_taraghi_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    taraghi = get_object_or_404(Taraghi, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "taraghi shahr Management System",
                'body': message,
                'click_action': reverse('taraghi_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': taraghi.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationTaraghi(taraghi=taraghi, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_tootia_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    tootia = get_object_or_404(Tootia, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "tootia shahr Management System",
                'body': message,
                'click_action': reverse('tootia_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': tootia.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationTootia(tootia=tootia, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_drug_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    drug = get_object_or_404(Drug, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "drug shahr Management System",
                'body': message,
                'click_action': reverse('drug_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': drug.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationDrug(drug=drug, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_gen_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    gen = get_object_or_404(Gen, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "gen shahr Management System",
                'body': message,
                'click_action': reverse('gen_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': gen.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationGen(gen=gen, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_iron_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    iron = get_object_or_404(Iron, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "iron shahr Management System",
                'body': message,
                'click_action': reverse('iron_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': iron.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationIron(iron=iron, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_ptro_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    ptro = get_object_or_404(Ptro, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "ptro shahr Management System",
                'body': message,
                'click_action': reverse('ptro_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': ptro.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationPtro(ptro=ptro, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_agriculture_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    agriculture = get_object_or_404(Agriculture, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "agriculture shahr Management System",
                'body': message,
                'click_action': reverse('agriculture_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': agriculture.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationAgriculture(agriculture=agriculture, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_research_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    research = get_object_or_404(Research, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "research shahr Management System",
                'body': message,
                'click_action': reverse('research_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': research.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationResearch(research=research, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    staff = get_object_or_404(Staff, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Sugar Management System",
                'body': message,
                'click_action': reverse('staff_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': staff.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStaff(staff=staff, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def delete_staff(request, staff_id):
    staff = get_object_or_404(CustomUser, staff__id=staff_id)
    staff.delete()
    messages.success(request, "Staff deleted successfully!")
    return redirect(reverse('manage_staff'))


def delete_sugar(request, sugar_id):
    sugar = get_object_or_404(CustomUser, sugar__id=sugar_id)
    sugar.delete()
    messages.success(request, "Sugar deleted successfully!")
    return redirect(reverse('manage_sugar'))


def delete_kh(request, kh_id):
    kh = get_object_or_404(CustomUser, kh__id=kh_id)
    kh.delete()
    messages.success(request, "Kh deleted successfully!")
    return redirect(reverse('manage_kh'))


def delete_person(request, person_id):
    try:
        person = CustomUser.objects.filter(id=person_id)
        person.delete()
        person.save()
        messages.success(request, "Person deleted successfully!")
    except:
        print(555)
        pass

    return redirect(reverse('manage_person'))




def delete_holding(request, holding_id):
    holding = get_object_or_404(Holding, id=holding_id)
    holding.delete()
    messages.success(request, "Holding deleted successfully!")
    return redirect(reverse('manage_holding'))



def delete_piran(request, piran_id):
    piran = get_object_or_404(CustomUser, piran__id=piran_id)
    piran.delete()
    messages.success(request, "Piran shahr deleted successfully!")
    return redirect(reverse('manage_piran'))


def delete_tomato(request, tomato_id):
    tomato = get_object_or_404(CustomUser, tomato__id=tomato_id)
    tomato.delete()
    messages.success(request, "Tomato deleted successfully!")
    return redirect(reverse('manage_tomato'))


def delete_taraghi(request, taraghi_id):
    taraghi = get_object_or_404(CustomUser, taraghi__id=taraghi_id)
    taraghi.delete()
    messages.success(request, "Taraghi shahr deleted successfully!")
    return redirect(reverse('manage_taraghi'))


def delete_tootia(request, tootia_id):
    tootia = get_object_or_404(CustomUser, tootia__id=tootia_id)
    tootia.delete()
    messages.success(request, "Tootia shahr deleted successfully!")
    return redirect(reverse('manage_tootia'))


def delete_drug(request, drug_id):
    drug = get_object_or_404(CustomUser, drug__id=drug_id)
    drug.delete()
    messages.success(request, "Drug shahr deleted successfully!")
    return redirect(reverse('manage_drug'))


def delete_gen(request, gen_id):
    gen = get_object_or_404(CustomUser, gen__id=gen_id)
    gen.delete()
    messages.success(request, "Gen shahr deleted successfully!")
    return redirect(reverse('manage_gen'))


def delete_iron(request, iron_id):
    iron = get_object_or_404(CustomUser, iron__id=iron_id)
    iron.delete()
    messages.success(request, "Iron shahr deleted successfully!")
    return redirect(reverse('manage_iron'))


def delete_ptro(request, ptro_id):
    ptro = get_object_or_404(CustomUser, ptro__id=ptro_id)
    ptro.delete()
    messages.success(request, "Ptro shahr deleted successfully!")
    return redirect(reverse('manage_ptro'))


def delete_agriculture(request, agriculture_id):
    agriculture = get_object_or_404(CustomUser, agriculture__id=agriculture_id)
    agriculture.delete()
    messages.success(request, "Agriculture shahr deleted successfully!")
    return redirect(reverse('manage_agriculture'))


def delete_research(request, research_id):
    research = get_object_or_404(CustomUser, research__id=research_id)
    research.delete()
    messages.success(request, "Research shahr deleted successfully!")
    return redirect(reverse('manage_research'))


def delete_organ(request, organ_id):
    organ = get_object_or_404(Organ, id=organ_id)
    try:
        organ.delete()
        messages.success(request, "Organ deleted successfully!")
    except Exception:
        messages.error(
            request,
            "Sorry, some sugars are assigned to this organ already. Kindly change the affected sugar organ and try again")
    return redirect(reverse('manage_organ'))


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, "Subject deleted successfully!")
    return redirect(reverse('manage_subject'))


def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    try:
        session.delete()
        messages.success(request, "Session deleted successfully!")
    except Exception:
        messages.error(
            request, "There are sugars assigned to this session. Please move them to another session.")
    return redirect(reverse('manage_session'))


def index(request):
    if request.method == 'POST':
        student = StudentForm(request.POST, request.FILES)
        if student.is_valid():
            Student.objects.create(file=request.FILES['file'], company=request.POST.get('company'),
                                   email=request.POST.get('email'), date=request.POST.get('date'),
                                   jalali_date=request.POST.get('jalali_date'),
                                   file_name=request.POST.get('file_name'),
                                   subject=request.POST.get('subject'))

            if handle_uploaded_file(request.FILES['file'], request.POST.get('company'), request.POST.get('email'),
                                    request.POST.get('date')) == True:
                return redirect(reverse('index'))
            else:
                return render(request, "hod_template/add_file_admin_template_error.html", {'form': student})
        else:
            return HttpResponse("error")
    else:
        student = StudentForm()
        return render(request, "hod_template/add_file_admin_template.html", {'form': student})
