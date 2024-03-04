from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']



# forms.py
from django import forms
from .models import Profile




from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class RegistrationProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'location', 'phone']
        widgets = {
            'firstname': forms.TextInput(attrs={'required': False}),
            'lastname': forms.TextInput(attrs={'required': False}),
            'location': forms.TextInput(attrs={'required': False}),
            'phone': forms.TextInput(attrs={'required': False}),
        }




class ProfileData(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'location', 'phone']
        widgets = {
            'firstname': forms.TextInput(attrs={'required': False}),
            'lastname': forms.TextInput(attrs={'required': False}),
            'location': forms.TextInput(attrs={'required': False}),
            'phone': forms.TextInput(attrs={'required': False}),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['username']
        if commit:
            user.save()
            # Automatically create a profile for the user
            Profile.objects.get_or_create(user=user)
        return user


# forms.py

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'profile_image', 'location', 'phone']
