from django.shortcuts import render, reverse, redirect
from .models import Vistor, Entry
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required()
def register_entry(request):
    """
            record new vistor log
    """
    template_to_load = "vistors/register_entry.html"
    context = {}
    if request.method == "POST":
        logged_in_user = request.user
        entry_data = request.POST
        try:
            with transaction.atomic():
                vistor = None
                vistor_id = entry_data['vistor'] if 'vistor' in entry_data else None
                # handle visitor
                if vistor_id is not None:
                    vistor = Vistor.objects.get(pk=vistor_id)
                else:
                    print("creating vistor")
                    vistor_data = {}
                    vistor_data['name'] = entry_data['name']
                    vistor_data['tel_number'] = entry_data['tel_number']
                    vistor_data['company'] = entry_data['company']
                    vistor_data['tenant'] = entry_data['tenant']
                    vistor_data['created_by'] = logged_in_user
                    vistor = Vistor(**vistor_data)
                    print(vistor_data)
                    valid, errors = vistor.validate()
                    print(valid)
                    if valid:
                        vistor.save()
                    else:
                        raise IntegrityError(errors)

                # create vistor entry log
                entry_log = {}
                entry_log['temperature'] = entry_data['temperature']
                entry_log['vistor'] = vistor
                entry_log['destination'] = entry_data['dest'] if 'dest' in entry_data else ""
                entry_log['created_by'] = logged_in_user
                new_entry = Entry(**entry_log)
                valid, errors = new_entry.validate()
                if valid:
                    new_entry.save()
                else:
                    raise IntegrityError(errors)

                return redirect(reverse("vistors:create"))

        except Exception as e:
            context['errors'] = str(e)
    return render(request, template_to_load, context)


@login_required()
def search_entry(request):
    """
            search entry logs
    """
    context = {}
    template_to_load = 'visitors/search_entry.html'
    if request.method == "POST":
        data = request.POST
        search_data = {}
        # filter relavant search parameters
        if data['name']:
            search_data['vistor__name'] = data['name']

        if data['temperature']:
            search_data['temperature__gte'] = data['temperature']

        # if data['from_date']:
        # 	search_data['time_stamp__gte'] = data[]
        query_result = Entry.objects.filter(**search_data)
        context['result'] = query_result
    return render(request, template_to_load, context)


@login_required()
def search_to_add(request):
    """
            searches person by phone number
    """
    template_to_load = 'vistors/search_to_add.html'
    context = {}
    if request.method == "POST":
        phone_number = request.POST['phone']
        try:
            vistor = Vistor.objects.get(tel_number=phone_number)
            context['vistor'] = vistor
        except Vistor.DoesNotExist:
            context['errors'] = "Visitor with provided phone number is not registered"
    return render(request, template_to_load, context)
