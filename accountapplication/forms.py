from django import forms
from accountapplication.models import Profile, Message


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_photo", "background_photo"]
        labels = {
            "profile_photo": "Profil Fotoğrafı",
            "background_photo": "Arkaplan Fotoğrafı",
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        labels = {
            "content": "",
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows':1}),
        }
