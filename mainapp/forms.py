from django import forms
from django.forms import Textarea
from accountapplication.models import Post, Comment


class CreatePost(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post_text'].required = False

    class Meta:
        model = Post
        fields = ("post_text",)


class CreateComment(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ("comment_text", )
        labels = {
            "comment_text": "",
        }
        widgets = {
            'comment_text': Textarea(attrs={'rows': 5, "placeholder": "Yorumunuz...",})
        }

