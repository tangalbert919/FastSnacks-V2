from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.get_username()
            return render(request, 'index.html', context={'username': username})
        return render(request, 'index.html')
