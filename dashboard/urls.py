from django.urls import path
from .views import DashboardView, LeaderboardView, SaveDataInJsonView, SearchUserAddressView, DocumentView


urlpatterns = [
    path('', DashboardView.as_view(), name='accounts_list'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('updatejson/', SaveDataInJsonView.as_view(), name='updatejson'),
    path('search/user-address', SearchUserAddressView.as_view(), name='search'),
    path('document', DocumentView.as_view(), name='document'),
]
