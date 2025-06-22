from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('',views.login,name='login'),
    path('forget/',views.forget,name='forget'),
    path('passwordchange/<token>/',views.update_password,name='update'),
    path('homepage/<token>/',views.homepage,name='homepage'),
    path('homepage/<token>/add_employee',views.add_employee,name='add_employee'),
    path('homepage/<token>/update',views.update,name='update'),
    path('homepage/<token>/delete',views.delete,name='delete'),
]
