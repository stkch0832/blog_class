from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogIndexView.as_view(), name='blog_index'),
    path('blog/', views.BlogListView.as_view(), name="blog_list"),
    path('blog/new/', views.BlogCreateView.as_view(), name="blog_new"),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name="blog_detail"),
    path('blog/<int:pk>/edit/', views.BlogUpdateView.as_view(), name="blog_update"),
    path('blog/<int:pk>/delete/', views.BlogDeleteView.as_view(), name="blog_delete"),
]
