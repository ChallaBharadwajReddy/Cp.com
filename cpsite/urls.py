from django.contrib import admin
from django.urls import include,path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomePage,name="home"),
    path('lockout/',include('lockout_page.urls'),name="lockout"),
    path('register/',views.RegisterPage,name="register"),
    path('login/',views.LoginPage,name="login"),
    path('logout/',views.logOut,name="logout"),
]
