from django.shortcuts import render, redirect
from .models import User, Profile
from .forms import ProfileForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.contrib import messages


class ProfileEdit(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        profile_data = Profile.objects.get(user_id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            request.FILES or None,
            initial = {
                'username': profile_data.username,
                'introduction': profile_data.introduction,
                'birth': profile_data.birth,
                # 'image': profile_data.image,
            }
        )
        return render(request, 'account/profile_form.html', context= {
            'profile_data': profile_data,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            print(form)
            try:
                profile_data = Profile.objects.get(user_id=request.user.id)
                profile_data.username = form.cleaned_data['username']
                profile_data.introduction = form.cleaned_data['introduction']
                profile_data.birth = form.cleaned_data['birth']
                # profile_data.image = form.cleaned_data['image']

                if 'image' in form.cleaned_data:
                    profile_data.image = form.cleaned_data['image']

                profile_data.save()
                messages.success(request, 'プロフィールを更新しました。')
                return redirect('accounts:profile_form')

            except ValidationError as e:
                form.add_error('birth', e)

        return render(request, 'account/profile_form.html', context= {
            'form': form,
        })
