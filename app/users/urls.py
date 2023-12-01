from django.urls import path
from .views import (UserProfilesView,
                    GetUpdateUserProfileView,
                    UserProfileView,
                    SearchUser)

urlpatterns = [
    path('list/', UserProfilesView.as_view(), name='user-profiles-view'),
    path('me/', GetUpdateUserProfileView.as_view(), name='get_update-user_profile'),
    path('<int:pk>/', UserProfileView.as_view(), name='get-specific-user_profile'),
    path('', SearchUser.as_view(), name='user-search'),
]
