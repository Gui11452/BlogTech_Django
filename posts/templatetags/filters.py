from django import template
from posts.models import Post
from comentarios.models import Comentario

register = template.Library()

@register.filter(name='comentarios_index')
def comentarios_index(post_id):
    comentarios = Comentario.objects.filter(publicado_comentario=True,
    post_comentario__id=post_id)
    print(len(comentarios))
    if len(comentarios) == 1:
        return f'{len(comentarios)} comentário'
    else:
        return f'{len(comentarios)} comentários'

@register.filter(name='numero_posts')
def numero_posts(num):
    if num == 0:
        return f'Nenhum post foi encontrado!'
    elif num == 1:
        return f'Foi encontrado 1 post!'
    else:
        return f'Foram encontrados {num} posts!'