from .models import General  

def general_info(request):
    general = General.objects.last()  
    return {
        'general': general,
    }