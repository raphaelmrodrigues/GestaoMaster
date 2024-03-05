from django.shortcuts import render
from usuario.models import Usuario
from django.http import HttpResponse
from django.shortcuts import redirect
from hashlib import sha256

# Create your views here.

def home(request):
    status = request.GET.get('status')
    usuario = Usuario.objects.get(id = request.session['usuario'])
    usuarios = Usuario.objects.all()
    return render(request, 'home.html', {'usuarios': usuarios,
                                         'usuario': usuario,
                                         'usuario_logado': request.session.get('usuario'),
                                         'status': status})

def excluir_usuario(request):
    usuario_nome = request.POST.get('usuario')
    usuario = Usuario(id = usuario_nome)
    user = Usuario.objects.get(id = usuario_nome)
    if user.nome == 'admin':
        return redirect('/home/home/?status=1')
    else:
        usuario.delete()
        return redirect('/home/home/?status=0')


def adicionar_usuario(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    email = request.POST.get('email')
    endereco = request.POST.get('endereco')
    idade = request.POST.get('idade')
    sexo = request.POST.get('sexo')
    usuario_logado = Usuario.objects.get(id = request.session['usuario'])
    if usuario_logado.nome == 'admin':
        usuario_email = Usuario.objects.filter(email=email)
        if len(usuario_email) > 0:
            return redirect('/home/home/?status=3')
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome = nome, senha = senha, email = email, endereco = endereco, idade = idade, sexo = sexo)
        usuario.save()
        return redirect('/home/home/?status=4')
    else:
        return redirect('/home/home/?status=2')


def editar_usuario(request):
    if request.method == 'POST':
        # Receber dados do formulário
        usuario_id = request.POST.get('usuario')
        usuario = Usuario.objects.get(id = usuario_id)
        senha = request.POST.get('senha')
        email = request.POST.get('email')

        # Atualizar dados no banco de dados

        usuario.email = request.POST.get('email')
        senha = sha256(senha.encode()).hexdigest()
        usuario.senha = senha
        usuario.endereco = request.POST.get('endereco')
        usuario.idade = request.POST.get('idade')
        usuario.sexo = request.POST.get('sexo')

        # Salvar as alterações
        usuario.save()

        # Redirecionar ou renderizar conforme necessário
        return redirect('/home/home/?status=6')
    else:
        # Se o método não for POST, renderize o formulário
        return render(request, 'home.html', {'usuarios': Usuario.objects.all()})
