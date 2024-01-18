from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', TemplateView.as_view(template_name='account/index.html')),

    path('profile/', views.ProfileEdit.as_view(), name='profile_form' ),

]
