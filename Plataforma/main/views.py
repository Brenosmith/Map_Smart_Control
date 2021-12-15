from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from .models import Category, Equipment, Status
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, StatusForm, EquipmentForm, UserProfileForm
from django.core import serializers
from django.core.mail import send_mail


# Create your views here.
def homepage(request):
    # return HttpResponse("Esta é a homepage")
    return render(request=request,
                  template_name="main/categories.html",
                  context={"categories": Category.objects.all})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")

            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = NewUserForm
    profile_form = UserProfileForm
    return render(request,
                  "main/register.html",
                  context={"form": form, "profile_form": profile_form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request, "main/login.html", {"form": form})


def single_slug_request(request, single_slug):
    access_username = None
    if request.user.is_authenticated:
        access_username = request.user.username

    categories = []
    for c in Category.objects.all():
        categories.append(c.category_slug)

    if single_slug in categories:
        # filtrar tutorial_category que aponta para category_slug
        if request.user.is_superuser:
            matching_equipments = Equipment.objects.filter(category_name__category_slug=single_slug)
        else:
            matching_equipments = Equipment.objects.filter(category_name__category_slug=single_slug).filter(
                equipment_user_username=request.user.username)

        return render(request=request,
                      template_name='main/equipment.html',
                      context={"equipments": matching_equipments.all, "username": access_username})

    status_ = []
    for s in Equipment.objects.all():
        status_.append(s.equipment_slug)

    if single_slug in status_:
        matching_status_ = Status.objects.filter(equipment_id__equipment_slug=single_slug)
        specific_equipment = Equipment.objects.filter(equipment_slug=single_slug)

        return render(request=request,
                      template_name='main/status.html',
                      context={"status_": matching_status_.all, "equipment": specific_equipment.all,
                               "username": access_username})

    return HttpResponse(f"{single_slug} does not correspond to anything we know of!")


def add_status(request):
    if request.method == "POST":
        form = StatusForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # img_obj = form.instance
            messages.success(request, "Status adicionado com sucesso!")
            return redirect("/")
    else:
        form = StatusForm()
    return render(request, "main/add_status.html", context={'form': form})


def add_equipment(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipamento adicionado com sucesso!")
            return redirect("/")
    else:
        form = EquipmentForm()
    return render(request, "main/add_equipment.html", context={'form': form})


def dashboard(request):
    if request.method == 'POST' and 'run_script' in request.POST:
        mail_company()

    return render(request, "main/dashboard.html", {})


def pivot_data(request):
    dataset = Equipment.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)


def pivot_data2(request):
    dataset = Status.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)


def mail_company():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    Superuser = User.objects.filter(is_superuser=True).values_list('email')
    Superuser_mail = None
    for i in Superuser:
        Superuser_mail = str(list(i)[0])

    equip_peritagem = Equipment.objects.filter(equipment_status="Peritagem")
    equip_manutencao = Equipment.objects.filter(equipment_status="Manutenção")

    from itertools import chain
    filtered_equip = chain(equip_manutencao, equip_peritagem)

    from datetime import date, timedelta
    one_week_ago = date.today() - timedelta(days=7)

    # loop para olhar todos equipamentos em perit. e manut.
    for equip_id in filtered_equip:
        # pega status de cada equipamento filtrado
        status = list(Status.objects.filter(equipment_id=equip_id))
        # pega queryset de status nao vazio destes equipamentos
        if status:
            most_recent_status = None
            # loop para percorrer todos os status nao vazios
            for next_stat in status:
                # pegar o mais novo dentro de cada grupo de stat
                if most_recent_status is None or most_recent_status.status_published.date() <= next_stat.status_published.date():
                    most_recent_status = next_stat
                    print('## É status mais recente do equipamento:', most_recent_status)
            # verifica se esta desatualizado ha mais de 7 dias o status mais recente filtrado
            if most_recent_status.status_published.date() <= one_week_ago:
                print("## Mais de 7 dias sem update:", most_recent_status.status_published.date(), "<", one_week_ago)
                id_to_mail = most_recent_status.equipment_id
                print("#### ID:", id_to_mail)
                this_id_equip = Equipment.objects.filter(equipment_id=str(id_to_mail))
                user_to_email = []
                mail_to_email = []
                # pega usuario do queryset
                for f in this_id_equip:
                    user_to_email.append(f.equipment_user_username)
                # pega e-mail do queryset
                for f in User.objects.filter(username=user_to_email[0]):
                    mail_to_email.append(f.email)
                print("#### User:", user_to_email)
                print("#### E-mail:", mail_to_email)

                # enviar e-mail
                subject = 'Atualize o status do equipamento'
                message = '''Prezado,

O status do equipamento com ID:''' + str(id_to_mail) + ''' não é atualizado há mais de uma semana,
pedimos por gentileza que acesse a plataforma o quanto antes e informe o
status atual.

Obrigado'''
                sent_by = Superuser_mail
                # sent_to = mail_to_email
                sent_to = ['ferraz.breno.g@gmail.com']

                try:
                    if not (sent_to is None):
                        sent_to = sent_to[0]
                        send_mail(subject, message, sent_by, [sent_to])
                except Exception as e:
                    print(e)
            else:
                print("## Menos de 7 dias sem update")
        else:
            print("## Status vazio")
            id_to_mail2 = equip_id.equipment_id
            print("#### ID:", id_to_mail2)
            this_id_equip2 = Equipment.objects.filter(equipment_id=str(id_to_mail2))
            user_to_email2 = []
            mail_to_email2 = []
            # pega usuario do queryset
            for f2 in this_id_equip2:
                user_to_email2.append(f2.equipment_user_username)
            # pega e-mail do queryset
            for f2 in User.objects.filter(username=user_to_email2[0]):
                mail_to_email2.append(f2.email)
            print("#### User:", user_to_email2)
            print("#### E-mail:", mail_to_email2)

            # enviar e-mail
            subject = 'Equipamento sem atualização'
            message = '''Prezado,

O status do equipamento com ID:''' + str(id_to_mail2) + ''' não recebeu nenhuma atualização,
pedimos por gentileza que acesse a plataforma o quanto antes e informe o status atual.

Obrigado'''
            sent_by = Superuser_mail
            # sent_to = mail_to_email2
            sent_to = ['ferraz.breno.g@gmail.com']

            try:
                if not (sent_to is None):
                    sent_to = sent_to[0]
                    send_mail(subject, message, sent_by, [sent_to])
            except Exception as e:
                print(e)
