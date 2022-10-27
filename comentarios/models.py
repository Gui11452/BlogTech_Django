from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from posts.models import Post

class Comentario(models.Model):
    nome_comentario = models.CharField(max_length=150, blank=True, null=True, verbose_name="Título")
    email_comentario = models.EmailField(verbose_name="E-mail")
    comentario = models.TextField(verbose_name="Detalhes")
    post_comentario = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Título do Post")
    usuario_comentario = models.ForeignKey(User, on_delete=models.CASCADE, 
    blank=True, null=True, verbose_name="Usuário")
    data_comentario = models.DateTimeField(default=timezone.now, verbose_name="Data")
    publicado_comentario = models.BooleanField(default=False, verbose_name="Publicado")

    def __str__(self):
	    return self.nome_comentario 
