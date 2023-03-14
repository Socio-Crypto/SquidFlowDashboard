from django.shortcuts import render
from django.views.generic import View

class DashboardView(View):

    def get(self, request):
        context = {}
        
        return render(request, 'dashboard.html', context=context)


class DashboardView1(View):

    def get(self, request):
        context = {}
        
        return render(request, 'dashboard_1.html', context=context)

class DashboardView12(View):

    def get(self, request):
        context = {}
        
        return render(request, 'dashboard.html', context=context)

class DashboardView3(View):

    def get(self, request):
        context = {}
        
        return render(request, 'dashboard.html', context=context)

class DashboardView4(View):

    def get(self, request):
        context = {}
        
        return render(request, 'dashboard.html', context=context)