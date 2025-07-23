from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
from main_app.models import Flag


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user  # Who is the current user ?
        if user.is_authenticated:

            if user.user_type == '1':  # Is it the HOD/Admin
                if modulename == 'main_app.sugar_views':
                    return redirect(reverse('admin_home'))

            elif user.user_type == '2':  # Staff :-/ ?
                if modulename == 'main_app.sugar_views' or modulename == 'main_app.hod_views':
                    return redirect(reverse('staff_home'))

            elif user.user_type == '3':  # ... or sugar ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('sugar_home'))

            elif user.user_type == '4':  # ... or Kh ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('kh_home'))

            elif user.user_type == '20':  # ... or Kh ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('person_home'))

            elif user.user_type == '5':  # ... or Kh ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('holding_home'))

            elif user.user_type == '6':  # ... or Kh ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('piran_home'))

            elif user.user_type == '7':  # ... or golfam ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('tomato_home'))

            elif user.user_type == '8':  # ... or golfam ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('taraghi_home'))

            elif user.user_type == '9':  # ... or Kh ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('tootia_home'))

            elif user.user_type == '10':  # ... or Kh ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('drug_home'))

            elif user.user_type == '11':  # ... or Kh ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('gen_home'))

            elif user.user_type == '12':  # ... or Kh ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('iron_home'))

            elif user.user_type == '13':  # ... or Kh ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('ptro_home'))

            elif user.user_type == '14':  # ... or Kh ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('agriculture_home'))

            elif user.user_type == '15':  # ... or Kh ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('research_home'))

            else:  # None of the aforementioned ? Please take the user to login page
                return redirect(reverse('login_page'))
        else:
            if request.path == reverse(
                    'login_page') or modulename == 'django.contrib.auth.views' or request.path == reverse(
                'user_login'):  # If the path is login or has anything to do with authentication, pass
                pass
            else:
                f = Flag.objects.all().get(id=1)
                if f.flag == True:
                    f.flag = False
                    f.save()
                    return redirect(reverse('login_page'))
