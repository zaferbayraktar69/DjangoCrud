
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.showIha,name="showIha"),
    path('Register',views.register,name="register"),
    path('Login',views.login,name="login"),
    path('InsertIha',views.insertIha,name="insertIha"),
    path('Edit/<int:id>',views.editIha,name="editIha"),
    path('Update/<int:id>',views.updateIha,name="updateIha"),
    path('Delete/<int:id>',views.delIha,name="delIha"),
    path('Logout',views.logout,name="logout"),
    path('InsertCategory',views.insertCategory,name="insertCategory"),

]
