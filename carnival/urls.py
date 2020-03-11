from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from carnival.rootapp import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('capture/',views.capture,name="capture"),

    path('user_recognise/', views.user_recognise, name='user_recognise'),
    path('camera_recognise/', views.camera_recognise, name='camera_recognise'),

    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name="login"),
    path('register/',views.register,name="register"),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name="logout"),

    path('users/', views.user_list, name='user_list'),



    path('users/upload/', views.upload_user, name='upload_user'),


    path('users/<int:pk>/', views.delete_user, name='delete_user'),


    path('edit_user/<int:pk>', views.edit_user, name='edit_user'),


    path('update/<int:pk>', views.update, name='update'),



    path('attend', views.attend, name='attend'),

    path('camera/upload/', views.upload_camera, name='upload_camera'),

    path('cameralist/<int:pk>/', views.delete_camera, name='delete_camera'),
    path('edit_camera/<int:pk>', views.edit_camera, name='edit_camera'),
    path('update_camera/<int:pk>', views.update_camera, name='update_camera'),
    path('cameralist/', views.cameralist, name='cameralist'),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
