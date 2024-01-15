from typing import Any
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from phonenumber_field.formfields import PhoneNumberField

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'id_email'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_first_name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_last_name'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_phone_number'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'id': 'username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'id': 'password1'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'id': 'password2'})

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password1'])
        
        # Save phone_number directly to the User model
        user_profile = UserProfile(phone_number=self.cleaned_data['phone_number'])
        if commit:
            user.save()
            user_profile.user = user
            user_profile.save()
        
        return user



class EditUserForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_phone_number'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_staff'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['is_superuser'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})

        self.helper = FormHelper()
        self.helper.form_class = 'row g-3'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_superuser',
            Submit('submit', 'Update Profile', css_class='btn btn-primary')
        )