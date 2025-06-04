# catalog/views.py

from django.http import HttpResponse

def index(request):
    return HttpResponse("Вы находитесь на главной странице каталога.")
