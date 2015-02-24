from django import forms


class RegistrationForm(forms.Form):

    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)))
    firstname = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)))
    lastname = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)))
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)))

class MatchForm(forms.Form):
    user = forms.IntegerField(label='user');

class ProfilePicForm(forms.Form):
    pic = forms.ImageField()