from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from messages import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def login_user(request):
    template_to_load = 'checkin_auth/views/login.html'
    context = {}
    if request.method == "POST":
        try:
            auth_name = request.POST['username']
            auth_password = request.POST['password']
        except KeyError:
            context['login_failed'] = messages.AUTHENTICATION_FIELDS_REQUIRED.format(
                "user name", "password")
            return render(request, template_to_load, context)

        user = authenticate(request, username=auth_name,
                            password=auth_password)
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect(reverse("user_management:home"))
        context['login_failed'] = messages.AUTHENTICATION_FAILED
    return render(request, template_to_load, context)


@login_required()
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect(reverse("checkin_auth:login"))
    return redirect(reverse("user_management:home"))
