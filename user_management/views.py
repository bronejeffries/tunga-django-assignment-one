from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from messages import messages
from django.db import IntegrityError
from vistors.models import Entry

# Create your views here.


@login_required()
def home(request):
    """
            user dashboard
    """
    context = {}
    template_to_load = 'user_management/views/home/index.html'
    context['entries'] = Entry.objects.all()
    return render(request, template_to_load, context)


@login_required()
def create_user(request):
    """
            creates new user
    """
    context = {}
    template_to_load = 'user_management/views/home/create_new_user.html'
    if request.method == "POST":
        try:
            user_data = {}
            user_data['first_name'] = request.POST['first']
            user_data['last_name'] = request.POST['last']
            user_data['username'] = request.POST['username']
            user_data['password'] = request.POST['password']
            user_data['is_staff'] = request.POST['admin']
            user_data['email'] = request.POST['email']
            user = User(**user_data)
            user.set_password(user_data['password'])
            user.save()
        except KeyError as e:
            context['message'] = str(e) + ' field is required'
        except IntegrityError as e:
            context['message'] = str(e)
        else:
            context['message'] = messages.USER_CREATED_SUCCESSFULLY
    return render(request, template_to_load, context)
