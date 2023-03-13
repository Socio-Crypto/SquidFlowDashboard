from django.shortcuts import render
from django.views.generic import View

from .services import get_wallet_activity

class DashboardView(View):

    def get(self, request):
        context = {}
        # a = get_wallet_activity()
        return render(request, 'dashboard.html', context=context)