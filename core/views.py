from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválido.")
    return redirect('/')


@login_required(login_url='/login/')
def lista_eventos(request):
    user = request.user
    eventos = Evento.objects.filter(usuario=user)
    dados = {'eventos': eventos}
    return render(request, 'agenda.html', dados)


@login_required(login_url='/login/')
def evento(request):
    evento_id = request.GET.get('id')
    dados = {}
    if evento_id:
        dados['evento'] = Evento.objects.get(id=evento_id)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('title')
        data_evento = request.POST.get('date')
        descricao = request.POST.get('description')
        usuario = request.user
        evento_id = request.POST.get('evento_id')
        if evento_id:
            Evento.objects.filter(id=evento_id).update(titulo=titulo,
                                                       data_evento=data_evento,
                                                       descricao=descricao)
        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  usuario=usuario)

    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, evento_id):
    usuario = request.user
    evento = Evento.objects.get(id=evento_id)
    if usuario == evento.usuario:
        evento.delete()
    return redirect('/')
