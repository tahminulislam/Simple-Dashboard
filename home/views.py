from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum

from .models import Order


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    # Already logged in
    if request.user.is_authenticated:

        # Staff / Admin
        if request.user.is_staff or request.user.is_superuser:
            return redirect("home")

        # Office User
        return redirect("office_dashboard")


    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )


        # =================================================
        # INVALID LOGIN
        # =================================================

        if user is None:

            return render(
                request,
                "home/login.html",
                {
                    "error": "Invalid username or password."
                }
            )


        # =================================================
        # ACCOUNT INACTIVE
        # =================================================

        if not user.is_active:

            return render(
                request,
                "home/login.html",
                {
                    "error": "Your account is inactive. Contact administrator."
                }
            )


        # =================================================
        # STAFF / ADMIN LOGIN
        # =================================================

        if user.is_staff or user.is_superuser:

            login(request, user)

            return redirect("home")


        # =================================================
        # OFFICE USER LOGIN
        # =================================================

        login(request, user)

        return redirect("office_dashboard")


    return render(
        request,
        "home/login.html"
    )


# =========================================================
# OFFICE USER DASHBOARD
# =========================================================

@login_required(login_url="/login/")
def office_dashboard(request):

    # Staff/Admin cannot access Office Dashboard

    if request.user.is_staff or request.user.is_superuser:

        return redirect("home")


    # User orders

    my_orders = Order.objects.filter(
        customer=request.user
    ).count()


    completed_orders = Order.objects.filter(
        customer=request.user,
        status="completed"
    ).count()


    pending_orders = Order.objects.filter(
        customer=request.user,
        status="pending"
    ).count()


    cancelled_orders = Order.objects.filter(
        customer=request.user,
        status="cancelled"
    ).count()


    # User revenue

    my_revenue = (
        Order.objects
        .filter(
            customer=request.user,
            status="completed"
        )
        .aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )


    # Recent orders

    recent_orders = (
        Order.objects
        .filter(
            customer=request.user
        )
        .order_by("-created_at")[:5]
    )


    context = {

        "my_orders": my_orders,

        "completed_orders": completed_orders,

        "pending_orders": pending_orders,

        "cancelled_orders": cancelled_orders,

        "my_revenue": my_revenue,

        "recent_orders": recent_orders,

    }


    return render(
        request,
        "home/user_dashboard.html",
        context
    )


# =========================================================
# CUSTOM ADMIN / STAFF DASHBOARD
# =========================================================

@login_required(login_url="/login/")
def home(request):

    # Office User cannot access Admin Dashboard

    if not request.user.is_staff and not request.user.is_superuser:

        return redirect("office_dashboard")


    # =====================================================
    # TOTAL USERS
    # =====================================================

    total_users = User.objects.count()


    # =====================================================
    # TOTAL ORDERS
    # =====================================================

    total_orders = Order.objects.count()


    # =====================================================
    # COMPLETED ORDERS
    # =====================================================

    completed_orders = Order.objects.filter(
        status="completed"
    ).count()


    # =====================================================
    # REVENUE
    # =====================================================

    revenue = (
        Order.objects
        .filter(
            status="completed"
        )
        .aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )


    # =====================================================
    # RECENT ORDERS
    # =====================================================

    recent_orders = (
        Order.objects
        .select_related("customer")
        .order_by("-created_at")[:5]
    )


    context = {

        "total_users": total_users,

        "total_orders": total_orders,

        "completed_orders": completed_orders,

        "revenue": revenue,

        "recent_orders": recent_orders,

    }


    return render(
        request,
        "home/dashboard.html",
        context
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    return redirect("login")