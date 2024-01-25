from django import forms
from .models import Post

class BlogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs["class"] = "form-control"
        super().__init__(*args, **kwargs)


    class Meta:
        model = Post
        fields =['title', 'content', 'image']
