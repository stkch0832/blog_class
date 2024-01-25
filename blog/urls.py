from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = 'blog'

urlpatterns = [
    path('', TemplateView.as_view(template_name="blog/index.html")),
    path('blog/', views.BlogListView.as_view(), name="blog_list"),
    path('blog/new', views.BlogCreateView.as_view(), name="blog_new"),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name="blog_detail"),
    path('blog/<int:pk>/edit', views.BlogUpdateView.as_view(), name="blog_update"),
    path('blog/<int:pk>/delete', views.BlogDeleteView.as_view(), name="blog_delete"),
]
