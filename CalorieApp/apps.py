from django.apps import AppConfig


class CalorieappConfig(AppConfig):
    name = 'CalorieApp'
    
    def ready(self):
        import CalorieApp.signals
        
