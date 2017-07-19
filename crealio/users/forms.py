from django import forms
from .models import User


class Step1(forms.Form):
    username = forms.CharField(label='Identifiant')
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    conf_password = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email')
    conf_email = forms.EmailField(label="Confirmer l'email")
    cgu = forms.BooleanField(label="J'accepte les conditions générales d'utilisations")

    def clean_username(self):
        user = User.objects.filter(username=self.cleaned_data['username'])
        if user:
            raise forms.ValidationError("Cet identifiant est déjà  utilisé par un utilisateur")
        else:
            return self.cleaned_data['username']

    def clean_conf_password(self):
        if self.cleaned_data['password'] == self.cleaned_data['conf_password']:
            return self.cleaned_data['password']
        raise forms.ValidationError("Vous n'avez pas entré deux fois le même mot de passe")

    def clean_conf_email(self):
        if self.cleaned_data['email'].lower() == self.cleaned_data['conf_email'].lower():
            return self.cleaned_data['email'].lower()
        raise forms.ValidationError("Vous n'avez pas entré deux fois la même adresse email")


class Step2(forms.ModelForm):
    first_name = forms.CharField(label='Prénom')
    last_name = forms.CharField(label='Nom')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'city', 'country', 'job']
