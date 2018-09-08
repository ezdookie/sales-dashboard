from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label='E-mail')
    password = forms.CharField(widget=forms.widgets.PasswordInput, required=True, label='Password')
