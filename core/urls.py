
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('welcome', views.home , name="homepage"),
    path('', views.homez , name="homepage_two"),
    path('/search/q/', views.result , name="search"),
    path('/login/', views.login_view , name='login'),
    path('/logout/', views.logoutuser, name='logout'),
    path('download_report/<int:disaster_id>/', views.download_report, name='download_report'),
    path('search/', views.search_disaster, name='search_disaster'),
    path('rainfall/', views.rain, name='rain'),
    path('disasyer/<int:pk>', views.view_disaster, name='view_disaster'),
    path('result/', views.results, name='result'),
    path('profile/<str:username>/', views.profile, name='profile_page'),
    path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
    path('update_profile_data/', views.update_profile_data, name='update_profile_data'),
    path('register/', views.register, name='register'),
    path('community/', views.community, name='community'),
    path('community/sec/', views.feedback, name='sec'),

    path('thread/<int:pk>/', views.thread_detail, name='thread_detail'),


    path('get-new-posts/<int:thread_id>/', views.get_new_posts, name='get_new_posts'),
    path('create-profile/', views.create_profile, name='create_profile'),


   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

