from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import View

class DashboardView(View):

    def get(self, request):
        context = {}
        
        return render(request, 'dashboard.html', context=context)