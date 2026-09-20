from django.contrib import admin
from django.urls import path

from home.views import (
    home,
    login_view,
    office_dashboard,
    logout_view,
)


urlpatterns = [

    # =====================================================
    # DJANGO ADMIN
    # =====================================================

    path(
        "admin/",
        admin.site.urls
    ),


    # =====================================================
    # OFFICE USER LOGIN
    # =====================================================

    path(
        "login/",
        login_view,
        name="login"
    ),


    # =====================================================
    # OFFICE USER DASHBOARD
    # =====================================================

    path(
        "office/",
        office_dashboard,
        name="office_dashboard"
    ),


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    path(
        "",
        home,
        name="home"
    ),


    # =====================================================
    # LOGOUT
    # =====================================================

    path(
        "logout/",
        logout_view,
        name="logout"
    ),

]