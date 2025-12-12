from django.urls import path
from .views import *
urlpatterns = [  

    path('', homepage_view, name='homepage'),
    path('login/', login_view, name='login'), 
    path('signup/', signup_view, name='signup'), 
    path('about/', about_view, name='about'),
    path('admin/topics/<int:pk>/delete/', delete_topic_view, name='delete_topic'),
    path('admin/topics/create/', create_topic_view, name='create_topic'),
    path('edit-topic/<int:topic_id>/', edit_topic_view, name='edit_topic'),
    path('update-topic/<int:topic_id>/', update_topic_view, name='update_topic'),
    path('add-topic/', add_topic_view, name='add_topic'),
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
    path('topic-view/<int:topic_id>/', topic_detail_view, name='generated_topic'),
    path('api/saved-topics/', get_saved_topics, name='get_saved_topics'),
    path('api/notes/', get_notes, name='get_notes'),
    path('api/likes/', get_likes, name='get_likes'),
    path('api/toggle-save/', toggle_save, name='toggle_save'),
    path('api/toggle-like/', toggle_like, name='toggle_like'),
    path('api/save-note/', save_note, name='save_note'),
    path('api/delete-note/', delete_note, name='delete_note'),
    path('api/update-note/', update_note, name='update_note'),
    
]
