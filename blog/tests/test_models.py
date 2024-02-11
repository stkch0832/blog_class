from django.test import TestCase
from blog.models import Post
from accounts.models import User


class PostModelTests(TestCase):
    def setUp(self):
        # テストユーザーを作成
        self.user = User.objects.create(
            email='test@example.com',
            password='testpassword'
        )
        self.user.save()

    def test_is_empty_post(self):
        """
        初期状態でのDB内の保存データを確認
        """
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 0)

    def test_post_creation(self):
        """
        新規投稿が正しく動作しているかをテスト
        """
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test Content',
            image='Test_image.jpg'
        )

        qs_counter = Post.objects.count()
        self.assertEqual(qs_counter, 1)
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'Test Content')
        self.assertEqual(self.post.image, 'Test_image.jpg')
        self.assertTrue(self.post.created_at)
        self.assertTrue(self.post.updated_at)
        print(f'created_at: {self.post.created_at}')
        print(f'updated_at: {self.post.updated_at}')
