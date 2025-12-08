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

    path('admin/topics/<int:pk>/delete/', delete_topic_view, name='delete_topic'),
    path('admin/topics/create/', create_topic_view, name='create_topic'),
    path('admin/topics/update/<int:pk>', update_topic_view, name='update_topic'),
    path('role/', role_view, name='role'),
    path('users/', users_view, name='users'),
    path('user_homepage/', user_homepage_view, name='user_homepage'),
    path('user_page/', user_page_view, name='user_page'),
    path('setting/', setting_view, name='setting'),
    path('editprofile/', editprofile_view, name='editprofile'),
    path('adminlogin/',adminlogin_view, name='adminlogin'),
    path('admin_page/', admin_view, name='admin_page'),
    path('delete_account/', delete_account_view, name='delete_account'),
    path('update-student/<int:pk>/', update_student_view, name='update_user'), # pk is student_id
    path('delete-student/<int:pk>/', delete_student_view, name='delete_user'), # pk is student_id


    ######################
    path('api/saved-topics/', get_saved_topics, name='get_saved_topics'),
    path('api/notes/', get_notes, name='get_notes'),
    path('api/likes/', get_likes, name='get_likes'),
    path('api/toggle-save/', toggle_save, name='toggle_save'),
    path('api/toggle-like/', toggle_like, name='toggle_like'),
    path('api/save-note/', save_note, name='save_note'),
    path('api/delete-note/', delete_note, name='delete_note'),
    path('api/update-note/', update_note, name='update_note'),
    #path('topics/', topics_view, name='topics'),
]