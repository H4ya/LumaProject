from django.urls import path
from .views import * 
urlpatterns = [
    path('', home_view, name='home'),  

    path('login/', login_view, name='login'),
    path('homepage/', homepage_view, name='homepage'),  
    path('signup/', signup_view, name='signup'), 
    path('algorthim/', algorthim_view, name='algorthim'),
    path('computer_org/', computer_org_view, name='computer_org'),
    path('history_computing/', history_computing_view, name='history_computing'),
    path('logic_proof/', logic_proof_view, name='logic_proof'),
    path('operating_systems/', operating_systems_view, name='operating_systems'),
    path('software_eng/', software_eng_view, name='software_eng'),
    path('about/', about_view, name='about'),



    path('role/', role_view, name='role'),
    path('users/', users_view, name='users'),
    path('user_homepage/', user_homepage_view, name='user_homepage'),
    path('user_page/', user_page_view, name='user_page'),
    path('setting/', setting_view, name='setting'),
    path('editprofile/', editprofile_view, name='editprofile'),
    path('adminlogin/',adminlogin_view, name='adminlogin'),
    path('admin_page/', admin_view, name='admin_page'),
    path('delete_account/', delete_account_view, name='delete_account'),


    ######################
    path('api/saved-topics/', get_saved_topics, name='get_saved_topics'),
    path('api/notes/', get_notes, name='get_notes'),
    path('api/likes/', get_likes, name='get_likes'),
    #path('topics/', topics_view, name='topics'),
]
