from django.urls import path
from users.views import *
from . import views




urlpatterns = [
    path('' , views.index , name="index" ),
    path('login/' , login_page , name="login" ),
    path('signup/' , signup_page , name="signup" ),
    #path('register/' , register_page , name="register"),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('history/' , history , name="history" ),
    path('materials/', materials, name='materials'),
    path('tutor/', tutor, name='tutor'),
    path('profile/', profile, name='profile'),
    path('activate/<email_token>/', activate_email, name="activate_email"),  
    path("edit_profile/", edit_profile, name="edit_profile"),

    
  
]

