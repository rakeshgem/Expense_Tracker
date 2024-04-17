from django.urls import path
from .views import Home, loginpage, signup, editprofile, expenses, acclogout, add_expense

urlpatterns = [
    path("", Home, name='home'),
    path("login/", loginpage, name='login'),
    path("signup/", signup, name='signup'),
    path("logout/", acclogout, name='logout'),
    path("editprofile/", editprofile, name='editprofile'),
    path("expenses/", expenses, name='expenses'),
    path("addexpense/", add_expense, name='addexpense'),
]
