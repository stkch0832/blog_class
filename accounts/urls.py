from django.urls import path
from django.views.generic import TemplateView

name_app = 'accounts'

urlpatterns = [
    path('', TemplateView.as_view(template_name='account/index.html')),
]
