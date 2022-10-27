from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post, Categoria
from comentarios.models import Comentario
from django.db.models import Q
from django.core.paginator import Paginator
import requests
from .chaves_recaptcha import chave_front_end, chave_back_end

def index(request):
    posts = Post.objects.order_by('-data_post').filter(publicado_post=True)
    comentarios = Comentario.objects.order_by('-data_comentario').filter(publicado_comentario=True)

    numero_posts = len(posts)

    paginator = Paginator(posts, 20)
    page = request.GET.get('p')
    posts = paginator.get_page(page)

    return render(request, 'index.html', {
        'posts': posts,
        'comentarios': comentarios,
        'numero_posts': numero_posts
    })


def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = Comentario.objects.order_by('-data_comentario').filter(publicado_comentario=True, 
    post_comentario__id=post_id)

    titulo = request.POST.get('titulo')
    email = request.POST.get('email')
    comentario = request.POST.get('comentario')
    recaptcha = request.POST.get('g-recaptcha-response')

    if not comentario or not email or not titulo:
        return render(request, 'post.html', {
            'post': post,
            'comentarios': comentarios,
            'num_comentarios': len(comentarios),
            'chave_front_end': chave_front_end
        })

    if len(titulo) < 4 or len(comentario) < 4:
        messages.error(request, 'O título e o comentário devem ter no mínimo 4 caracteres!')
        return render(request, 'post.html', {
            'post': post,
            'comentarios': comentarios,
            'num_comentarios': len(comentarios),
            'chave_front_end': chave_front_end
        })

    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'post.html', {
            'post': post,
            'comentarios': comentarios,
            'num_comentarios': len(comentarios),
            'chave_front_end': chave_front_end
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': chave_back_end,
            'response': recaptcha
        }
    )
    recaptcha_result = recaptcha_request.json()
    
    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
        return render(request, 'post.html', {
            'post': post,
            'comentarios': comentarios,
            'num_comentarios': len(comentarios),
            'chave_front_end': chave_front_end
        })

    coment = Comentario(nome_comentario=titulo, email_comentario=email, comentario=comentario,
    usuario_comentario=request.user, post_comentario=post)
    coment.save()

    messages.success(request, 'O seu comentário foi enviado para a análise. Se for aprovado, será publicado!')
    return render(request, 'post.html', {
        'post': post,
        'comentarios': comentarios,
        'num_comentarios': len(comentarios),
        'chave_front_end': chave_front_end
    })


def categoria(request, categoria):
    posts = Post.objects.order_by('-data_post').filter(publicado_post=True, 
    categoria_post__nome_cat__iexact=categoria)

    numero_posts = len(posts)

    paginator = Paginator(posts, 20)
    page = request.GET.get('p')
    posts = paginator.get_page(page)

    return render(request, 'categoria.html', {
        'posts': posts,
        'numero_posts': numero_posts
    })

def busca(request):
    termo = request.GET.get('termo')

    if not termo:
        termo = ''

    posts = Post.objects.filter(
        Q(titulo_post__icontains=termo) |
        Q(autor_post__username__icontains=termo) |
        Q(conteudo_post__icontains=termo) |
        Q(excerto_post__icontains=termo) |
        Q(categoria_post__nome_cat__iexact=termo)
    )

    numero_posts = len(posts)

    paginator = Paginator(posts, 20)
    page = request.GET.get('p')
    posts = paginator.get_page(page)

    comentarios = Comentario.objects.order_by('-data_comentario').filter(publicado_comentario=True)
    return render(request, 'busca.html', {
        'posts': posts,
        'comentarios': comentarios,
        'numero_posts': numero_posts
    })


