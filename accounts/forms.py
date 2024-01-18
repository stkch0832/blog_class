from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from datetime import date

User = get_user_model()


class ProfileForm(forms.ModelForm):
    introduction = forms.CharField(
        label='自己PR',
        required=False,
        widget=forms.Textarea()
    )

    birth = forms.DateField(
        label='生年月日',
        required=False,
        widget=forms.NumberInput(attrs={
            'type': 'date',
        })
    )


    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs["class"] = "form-control"
        super().__init__(*args, **kwargs)

    def clean_birth(self):
        birth = self.cleaned_data["birth"]
        today = date.today()
        if birth is not None and birth >= today:
            raise forms.ValidationError('正しい日付を入力してください')

        return birth

    def clean_image(self):
        image = self.cleaned_data["image"]
        if image == False:
            image = ""

        return image


    class Meta:
        model = Profile
        exclude = ('user',)
