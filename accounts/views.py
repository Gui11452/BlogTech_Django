from email.headerregistry import Group
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def profile(request):
    if not request.user.is_authenticated:
        return redirect('index')

    return render(request, 'profile.html')

def edit(request):
    if not request.user.is_authenticated:
        return redirect('index')

    if request.method != 'POST':
        return render(request, 'edit.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    usuario = request.POST.get('usuario')
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not usuario or not senha1 or not senha2:
        messages.error(request, 'Nenhum campo pode ficar vazio!')
        return render(request, 'edit.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'O usuário inserido já está atrelado a uma conta!')
        return render(request, 'edit.html')

    if len(usuario) < 7 or len(usuario) > 14:
        messages.error(request, 'O usuário só pode ter entre 7 e 14 caracteres!')
        return render(request, 'edit.html')

    if senha1 != senha2:
        messages.error(request, 'As senhas tem que ser iguais!')
        return render(request, 'edit.html')

    if len(senha1) < 8:
        messages.error(request, 'A senha tem que ter no mínimo 8 caracteres!')
        return render(request, 'edit.html')

    user = User.objects.get(email=request.user.email)
    user.first_name = nome
    user.last_name = sobrenome
    user.username = usuario
    user.set_password(senha1)
    messages.success(request, 'Usuário editado com sucesso!')
    user.save()

    return redirect('profile')
    

def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method != 'POST':
        return render(request, 'login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'login.html')

    auth.login(request, user)
    return redirect('index')

def logout(request):
    if not request.user.is_authenticated:
        return redirect('index')
    
    auth.logout(request)
    messages.success(request, 'Usuário desconectado!')
    return redirect('login')


def registro(request):
    if request.user.is_authenticated and request.user.username != 'Guilherme11452':
        return redirect('index')

    message = 'O admin está logado. Todas as contas criadas aqui receberão a permissão para adicionar posts!'
    
    if request.user.username == 'Guilherme11452' and request.method != 'POST':
        messages.info(request, message)

    if request.method != 'POST':
        return render(request, 'registro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not usuario or not email or not senha1 or not senha2:
        messages.error(request, 'Nenhum campo pode ficar vazio!')
        return render(request, 'registro.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'O e-mail inserido é inválido')
        return render(request, 'registro.html')

    if User.objects.filter(username=usuario, email=email).exists():
        messages.error(request, 'O usuário e e-mail inseridos já estão atrelados a uma conta!')
        return render(request, 'registro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'O usuário inserido já está atrelado a uma conta!')
        return render(request, 'registro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'O e-mail inserido já está atrelado a uma conta!')
        return render(request, 'registro.html')

    if len(usuario) < 7 or len(usuario) > 14:
        messages.error(request, 'O usuário só pode ter entre 7 e 14 caracteres!')
        return render(request, 'registro.html')

    if senha1 != senha2:
        messages.error(request, 'As senhas tem que ser iguais!')
        return render(request, 'registro.html')

    if len(senha1) < 8:
        messages.error(request, 'A senha tem que ter no mínimo 8 caracteres!')
        return render(request, 'registro.html')

    messages.success(request, 'Usuário criado com sucesso!')

    if request.user.username == 'Guilherme11452':
        user = User.objects.create_user(first_name=nome, last_name=sobrenome, username=usuario,
    email=email, password=senha1, is_staff=True)
    else:
        user = User.objects.create_user(first_name=nome, last_name=sobrenome, username=usuario,
    email=email, password=senha1)

    user.save()

    autor = Group.objects.get(name='autor')

    if request.user.username == 'Guilherme11452':
        user.groups.clear()
        user.groups.add(autor)

    return redirect('login')


