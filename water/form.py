from django import forms
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

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



#for Registration Form with UserCreationForm class which is import above
class MyRegistrationForm(UserCreationForm):
    #for email field
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput,
                                 label='new password',
                                 )
    password2 = forms.CharField(widget=forms.PasswordInput,
                                 label='Re-enter password',
                                )
    #for field choose you want
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    #save from post(commit) in database
    
    def save(self, commit=True):
        #super-
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


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
        