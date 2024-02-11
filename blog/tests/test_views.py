from django.test import TestCase
from django.urls import reverse
import math
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Post
from django.contrib.auth import get_user_model


User = get_user_model()
signup_url = reverse("account_signup")
login_url = reverse("account_login")


class TestBlogIndexView(TestCase):
    def test_blog_index_view(self):
        """
        アクセスした際にステータスコード:200 であることを検証
        """
        response = self.client.get(reverse('blog:blog_index'))
        self.assertEqual(response.status_code, 200)


class TestBlogListView(TestCase):
    fixtures = [
        'users_testdata.json',
        'post_testdata.json',  # オブジェクト数: 12
    ]

    def test_blog_list_view(self):
        """
        アクセスした際に以下であることを検証
        ・ステータスコード: 200
        ・'blog/blog_list.html'をレンダリング
        """
        response = self.client.get(reverse('blog:blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')

    def test_blog_list_queryset(self):
        """
        正しいデータがクエリセットとして取得されているかを検証
        """
        response = self.client.get(reverse('blog:blog_list'))
        self.assertTrue('posts' in response.context)
        self.assertTrue(response.context['posts'].exists())

    def test_blog_list_view_pagination(self):
        """
        ページネーションにおいて、以下を検証
        ・contextに'paginator'が含まれているか
        ・contextに'page_obj'が含まれているか
        ・取得したデータがページネーションされているか
        ・総ページ数がクエリで取得したアイテムを'paginate_by'で除算した値と等しいか
        """
        response = self.client.get(reverse('blog:blog_list'))

        paginator = response.context['paginator']
        page_obj = response.context['page_obj']

        self.assertTrue('paginator' in response.context)
        self.assertTrue('page_obj' in response.context)

        num_items = page_obj.paginator.count
        num_pages = paginator.num_pages
        paginate_by = 5
        cal_pages = math.ceil(num_items / paginate_by)

        self.assertEqual(num_items, 12)
        self.assertEqual(num_pages, cal_pages)


class TestBlogCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test0000',
        )

    def test_blog_create_get_logged_in(self):
        """
        アクセスした際に以下であることを検証
        ・ステータスコード: 200
        ・'blog/blog_form.html'をレンダリング
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('blog:blog_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_form.html')

    def test_blog_create_get_not_logged_in(self):
        """
        アクセスした際に以下であることを検証
        ・ステータスコード: 302
        ・'accounts/login/'にリダイレクト
        """
        response = self.client.get('/blog/new/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/blog/new/')

    def test_blog_create_post(self):
        """
        フォームを送信した際に以下であることを検証
        ・ステータスコード: 302
        ・'blog/'にリダイレクト
        """
        self.client.force_login(self.user)
        data = {
            'title': 'Test title',
            'content': 'Test content',
            'image': 'Test image',
        }
        response = self.client.post(reverse('blog:blog_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog/')

    def test_blog_create_save(self):
        """
        フォームから送信されたデータが、正しくDBに保存されているかを検証
        """
        self.client.force_login(self.user)

        with open('media/test_blog/upload_pict/1/test_image.jpg', 'rb') as f:
            image_data = f.read()

        image = SimpleUploadedFile(
            "test_image.jpg",
            image_data,
            content_type="image/jpeg"
        )
        data = {
            'title': 'Test title',
            'content': 'Test content',
            'image': image,
        }
        response = self.client.post(reverse('blog:blog_new'), data)

        post_data = Post.objects.first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        self.assertIsNotNone(post_data)
        post_data = Post.objects.get(title='Test title')
        self.assertEqual(post_data.author.email, self.user.email)
        self.assertEqual(post_data.title, 'Test title')
        self.assertEqual(post_data.content, 'Test content')
        self.assertIsNotNone(post_data.image)
        self.assertIsNotNone(post_data.created_at)
        self.assertIsNotNone(post_data.updated_at)


class TestBlogUpdateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test0000',
        )

        self.instance = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test Content',
            image='Test_image.jpg'
        )

    def test_blog_update_get_not_logged_in(self):
        """
        アクセスした際に以下であることを検証
        ・ステータスコード: 302
        ・'accounts/login/'にリダイレクト
        """
        response = self.client.get(reverse('blog:blog_update', kwargs={'pk': self.instance.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/blog/{self.instance.pk}/edit/')

    def test_blog_update_get_correct_data(self):
        """
        アクセスした際に、該当データが正しく抽出・表示されているかを検証
        """
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('blog:blog_update', kwargs={'pk': self.instance.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.instance.title)

    def test_post_form_data_updated(self):
        """
        フォームのデータが正しく送信された場合に、更新が成功することを確認するテスト。
        """
        self.client.force_login(self.user)
        new_title = 'Updated title'
        form_data = {
            'title': new_title,
            'content': self.instance.content,
        }
        response = self.client.post(reverse('blog:blog_update', kwargs={
                                    'pk': self.instance.pk}), form_data)

        self.assertEqual(response.status_code, 302)
        updated_instance = Post.objects.get(pk=self.instance.pk)

    def test_invalid_form_data_does_not_update_object(self):
        """
        フォームのデータが不正である場合に、エラーメッセージが表示されることを確認するテスト。
        """
        self.client.force_login(self.user)
        form_data = {
            'title': '',
            'content': self.instance.content,
        }
        response = self.client.post(reverse('blog:blog_update', kwargs={
                                    'pk': self.instance.pk}), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'このフィールドは必須です。')

    def test_redirects_to_success_url_on_success(self):
        """
        データの更新後に、正しいリダイレクト先に移動することを確認するテスト。
        """
        self.client.force_login(self.user)
        form_data = {
            'title': 'Update title',
            'content': 'Update content',
        }
        response = self.client.post(reverse('blog:blog_update', kwargs={'pk': self.instance.pk}), form_data)
        self.assertRedirects(response, reverse('blog:blog_detail', kwargs={'pk': self.instance.pk}))


class TestBlogDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test0000',
        )

        self.instance = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test Content',
            image='Test_image.jpg'
        )

    def test_not_login_user_redirected_from_delete_view(self):
        """
        ログインしていないユーザーが削除を試みた場合に、正しいリダイレクト先に移動することを検証
        """
        self.client.logout()
        response = self.client.post(reverse('blog:blog_delete', kwargs={'pk': self.instance.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/blog/{self.instance.pk}/delete/')

    def test_delete_view_redirects_correctly(self):
        """
        ユーザーが削除をリクエストした際に、正しいリダイレクト先に移動することを検証
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse('blog:blog_delete', kwargs={'pk': self.instance.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:blog_list'))

    def test_deleted_data_does_not_exist(self):
        """
        削除された後に、データが存在しないことを検証
        """
        self.client.force_login(self.user)
        self.client.post(reverse('blog:blog_delete', kwargs={'pk': self.instance.pk}))
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=self.instance.pk)
