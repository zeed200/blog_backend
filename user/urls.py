from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register/', views.CreateUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('profile_update/', views.ProfileUpdate.as_view(), name='profile_update'),] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
