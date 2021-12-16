from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=200, verbose_name="Nome da Empresa")
    phone = models.IntegerField(verbose_name="Telefone de Contato")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Perfil Usuário"


class Category(models.Model):
    category_name = models.CharField(max_length=200, verbose_name="Categoria")
    category_summary = models.CharField(max_length=200)
    category_slug = models.CharField(max_length=200, default=1)

    class Meta:
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.category_name


class Equipment(models.Model):
    status_choices = (("Peritagem", "Peritagem"), ("Manutenção", "Manutenção"), ("Finalizado", "Finalizado"))

    equipment_id = models.IntegerField(verbose_name="ID do Equipamento")
    equipment_name = models.CharField(max_length=100, verbose_name="Nome Equipamento")
    category_name = models.ForeignKey(Category, default=1, verbose_name="Categoria",
                                      on_delete=models.SET_DEFAULT)
    equipment_summary = models.CharField(max_length=200, verbose_name="Descrição resumida")
    equipment_slug = models.CharField(max_length=200, default=1, verbose_name="Ref. URL - Usar o mesmo que o ID")
    equipment_status = models.CharField(max_length=10, choices=status_choices, blank=False, null=False,
                                        verbose_name="Status da operação")
    equipment_published = models.DateTimeField("Data da atualização", default=datetime.now())
    equipment_company = models.CharField(max_length=100, verbose_name="Empresa terceira")
    equipment_user_username = models.CharField(max_length=50, verbose_name="Nome de usuário")

    class Meta:
        verbose_name_plural = "Equipamentos"

    def __str__(self):
        return str(self.equipment_id)


class Status(models.Model):
    status_choices = (("Peritagem", "Peritagem"), ("Manutenção", "Manutenção"), ("Finalizado", "Finalizado"))

    status_title = models.CharField(max_length=200, verbose_name="Resumo/Título", blank=False)
    status_slug = models.CharField(max_length=200, default=1)
    status_content = models.TextField(verbose_name="Descrição", blank=False)
    status_published = models.DateTimeField("Data da atualização", default=datetime.now())
    equipment_id = models.ForeignKey(Equipment, default=1, verbose_name="Equipamento",
                                     on_delete=models.SET_DEFAULT)
    status_image = models.ImageField(blank=True, null=True, verbose_name="Imagem")
    status_situation = models.CharField(max_length=10, choices=status_choices, blank=False, null=False,
                                        verbose_name="Status da operação")

    class Meta:
        verbose_name_plural = "Atualizações"

    def __str__(self):
        return self.status_title
