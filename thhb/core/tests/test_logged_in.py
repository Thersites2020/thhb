"""
Tests that a logged-in user gets an appropriate response from all pages
"""

from django.test import TestCase
from django.urls import reverse
from core.models import BlogPost
from accounts.models import CustomUser

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


class LoggedInWriteAccessTests(TestCase):
    """
    Tests that a logged-in user can get all pages, including content
    appropriate for a user with write access
    """
    fixtures = ['fixtures/postdata.json']

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            write_access=True,
        )
        self.client.force_login(self.user)

    def tearDown(self):
        pass

    def test_intro_post_write_access(self):
        response = self.client.get("/introduction/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'single_post.html')
        self.assertContains(response, "Introduction")
        self.assertContains(response, ">Edit Post</a>")
        self.assertNotEqual(response, "I can't feel anything below my cummerbund")

    def test_second_post_write_access(self):
        response = self.client.get("/a-second-post/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'single_post.html')
        self.assertContains(response, "A Second Post")
        self.assertContains(response, ">Edit Post</a>")
        self.assertNotContains(response, "Release the hounds")

    def test_book_page_write_access(self):
        response = self.client.get("/the-book/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thebook.html')
        self.assertContains(response, "The Book")
        self.assertContains(response, ">Edit Post</a>")
        self.assertNotContains(response, "Ever since the dawn of time, man has yearned to destroy the sun")

    def test_homepage_write_access(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, "This Has Happened Before")
        self.assertContains(response, ">Logout</a>")
        self.assertNotContains(response, "See my loafers, former goafers")

    def test_homepage_url_write_access(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, "This Has Happened Before")
        self.assertContains(response, ">Logout</a>")
        self.assertNotContains(response, "Were you saying Boo-urns?")

    def test_post_list_write_access(self):
        response = self.client.get(reverse("core:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post_list.html")
        self.assertContains(response, "List of Posts")
        self.assertContains(response, ">Logout</a>")
        self.assertNotContains(response, "Seeing nothing but slack-jawed gawkers...")

    def test_post_list_url_write_access(self):
        response = self.client.get('/post_list')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post_list.html")
        self.assertContains(response, "List of Posts")
        self.assertContains(response, ">Logout</a>")
        self.assertNotContains(response, "I can't take much more of your blundering numbskullery")

    def test_user_page_write_access(self):
        response = self.client.get(reverse("core:user_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "userpage.html")
        self.assertContains(response, "User Page for")
        self.assertNotContains(response, "No Write Access")

    def test_user_page_url_write_access(self):
        response = self.client.get('/userpage')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "userpage.html")
        self.assertContains(response, "Create New Post")
        self.assertNotContains(response, "Cannot change password")


class LoggedInNoWriteAccessTests(TestCase):
    """
    Tests that a logged-in user without write access does not see content
    meant only for a user with write access
    """
    fixtures = ['fixtures/postdata.json']

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            write_access=False,
        )
        self.client.force_login(self.user)

    #def tearDown(self):
    #    pass

    def test_user_page_url_no_write_access(self):
        response = self.client.get('/userpage')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "userpage.html")
        self.assertContains(response, "Cannot write or edit posts")
        self.assertNotContains(response, "Create New Post")

    def test_intro_post_no_write_access(self):
        response = self.client.get("/introduction/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'single_post.html')
        self.assertContains(response, "Introduction")
        self.assertNotContains(response, ">Edit Post</a>")

    def test_book_page_no_write_access(self):
        response = self.client.get("/the-book/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thebook.html')
        self.assertContains(response, "The Book")
        self.assertNotContains(response, ">Edit Post</a>")


