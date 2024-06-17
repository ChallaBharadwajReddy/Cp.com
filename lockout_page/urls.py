from django.urls import path
from . import views

urlpatterns=[
    path("",views.MakeaMatch),
    path("contest/<int:pk>",views.lockout,name="contest")
]