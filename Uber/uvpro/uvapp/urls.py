from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('su/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('si/', views.signin, name='signin'),
    path('so/', views.signout, name='signout'),
    path('ho/', views.home, name='home'),
    path('dr/', views.drive, name="drive"),
    path('re/', views.rent, name='rent')
    # path('products/', views.List_and_Create_Data.as_view()),
    # path('products/<int:pk>', views.Retrieve_Update_Delete_Data.as_view())
]