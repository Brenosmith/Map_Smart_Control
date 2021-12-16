from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Status, Category, Equipment, UserProfile


class NewUserForm(UserCreationForm):
    # email = forms.EmailField(required=True, label="E-mail")
    # company = forms.CharField(max_length=200, required=True, label="Nome da Empresa")
    # phone = forms.IntegerField(required=True, label="Telefone de Contato")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ("company", "phone")


class StatusForm(ModelForm):
    status_category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Status
        # fields = '__all__'
        fields = ['status_title', 'status_situation', 'status_category', 'equipment_id', 'status_content', 'status_image']


class EquipmentForm(ModelForm):
    # status_category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Equipment
        fields = '__all__'
        # fields = ['status_title', 'status_category', 'equipment_id', 'status_content', 'status_image']
