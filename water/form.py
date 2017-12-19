from django import forms
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import UserProfile
from django.core.validators import validate_email

User=get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class MyRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
                attrs={'class': 'form-control'}
                ), required=True, max_length=30)
    email = forms.CharField(widget=forms.EmailInput(
            attrs={'class': 'form-control'}
            ), required=True, max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(
                attrs={'class': 'form-control'}
                ), required=True, min_length=8)
    confrm_password = forms.CharField(widget=forms.PasswordInput(
                     attrs={'class': 'form-control'}
                    ), required=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        try:
            check_email = validate_email(email)
        except:
            raise forms.ValidationError("Email is not correct format")
        return email
    def clean_confrm_password(self):
        password = self.cleaned_data['password']
        confrm_password = self.cleaned_data['confrm_password']
        if password and confrm_password:
            if password != confrm_password:
                raise forms.ValidationError("password did not match")





class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = (
                'Name',
                'address',
                'city',
                'state',
                'pin_code',
                'mobile_no',
            )

'''class Pincode(forms.Form):
    pin_code = forms.CharField(max_length=6, required=True)

    def clean(self):
        pin_code = self.cleaned_data.get('pin_code')
        if not pin_code:
            raise ValidationError("Not available")
        return pin_code
    '''
class EditProfile(UserChangeForm):

    class Meta:
        model = UserProfile
        fields = (
            'Name',
            'address',
            'city',
            'state',
            'pin_code',
            'mobile_no',
            'password',
        )
        