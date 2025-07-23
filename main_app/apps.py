from django.apps import AppConfig


class MainAppConfig(AppConfig):
    #خط زیر برای جلوگیری از ارور Auto-created primary key است
    default_auto_field = 'django.db.models.AutoField'

    name = 'main_app'
