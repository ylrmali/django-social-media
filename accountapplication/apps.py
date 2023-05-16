from django.apps import AppConfig


class AccountapplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accountapplication'

    ''' we import under the ready function because after the import signal, 
        all application should be install '''
    def ready(self):
        import accountapplication.signals