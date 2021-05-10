from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from auth_.views import MainUsersListApiView, ProfileApiView
urlpatterns = [
    path('api-token-auth/', obtain_jwt_token),
    path('users/', MainUsersListApiView.as_view()),
    path('profiles/<int:pk>/', ProfileApiView.as_view())
]
