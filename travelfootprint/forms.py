from django import forms


class ProfileForm(forms.Form):
    name = forms.CharField(label="Enter your instagram handle to find out your score!")
