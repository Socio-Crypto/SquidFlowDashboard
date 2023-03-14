from django.urls import path
from .views import DashboardView, DashboardView1


urlpatterns = [
    path('', DashboardView.as_view(), name='accounts_list'),
    path('1', DashboardView1.as_view(), name='accounts_list_1'),

]
