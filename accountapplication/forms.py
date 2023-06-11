from django import forms
from accountapplication.models import Profile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_photo", "background_photo"]
        labels = {
            "profile_photo": "Profil Fotoğrafı",
            "background_photo": "Arkaplan Fotoğrafı",
        }