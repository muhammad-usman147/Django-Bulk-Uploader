from django.urls import path
from .views import LoginView ,signup_view,  LogoutView, CustomProfile

urlpatterns = [

    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get-all-date/',CustomProfile.as_view(),name='display')

]
