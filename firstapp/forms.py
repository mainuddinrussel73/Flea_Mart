from django.contrib.auth.models import User
from django import forms
from firstapp.models import UserProfileInfo
from django.views.generic.edit import UpdateView



class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())


    class Meta():
        model = User
        fields = ('username','email','password')

class UserProfileInform(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('address','portfolio','profilepic','coverpic')



        