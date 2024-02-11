from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from ..views import (
    BlogIndexView,
    BlogListView,
    BlogCreateView,
    BlogDetailView,
    BlogUpdateView,
    BlogDeleteView,
)

class TestUrls(TestCase):
    def test_blog_index_view(self):
        """
        'blog:blog_index' を逆引きし、view が実行されるかを確認
        """
        response = self.client.get(reverse('blog:blog_index'))
        self.assertEqual(response.status_code, 200)

    def test_blog_index_template(self):
        """
        URL path("")にアクセスした際に、"blog/index.html" がレンダリングされるかを確認
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, "blog/index.html")

    
