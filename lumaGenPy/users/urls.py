from django.urls import path
from .views import home_view, login_view , homepage_view, signup_view 

urlpatterns = [
    path('', home_view, name='home'),  

    path('login/', login_view, name='login'),
    path('homepage/', homepage_view, name='homepage'),  
    path('signup/', signup_view, name='signup'), 
    
]
