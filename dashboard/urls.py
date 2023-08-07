from django.urls import path
from .views import DashboardView, LeaderboardView, SaveDataInJsonView, SearchUserAddressView, DocumentationView


urlpatterns = [
    path('', DashboardView.as_view(), name='accounts_list'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('updatejson/', SaveDataInJsonView.as_view(), name='updatejson'),
    path('search/user-address', SearchUserAddressView.as_view(), name='search'),
    path('Documentation', DocumentationView.as_view(), name='Documentation'),
]
