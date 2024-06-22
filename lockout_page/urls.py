from django.urls import path
from . import views

urlpatterns=[
    path("",views.MakeaMatch),
    path("worker",views.Worker,name="worker"),
    path("contest/<int:pk>",views.lockout,name="contest")
]