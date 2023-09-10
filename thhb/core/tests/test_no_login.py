from django.test import TestCase
from django.urls import resolve
from core.views import home

class NoLoginTest(TestCase):
    """
    To start, the entire blog is going to be available to logged-in users only, so pretty
    much every page should redirect to the under_construction template.
    """
    def test_home_page_no_login(self):
        # follow=True means that the test follows through to the (no-) login redirect URL
        response = self.client.get('', follow=True)
        #print(response.__dict__)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'under_construction.html')
        self.assertContains(response, "This site is under construction")
        self.assertNotContains(response, "Ancient Athens")

    def test_post_list_page_no_login(self):
        response = self.client.get('/post_list/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'under_construction.html')
        self.assertContains(response, "This site is under construction")
        self.assertNotContains(response, "Ancient Athens")

    def test_create_post_page_no_login(self):
        response = self.client.get('/create_post/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'under_construction.html')
        self.assertContains(response, "This site is under construction")
        self.assertNotContains(response, "Ancient Athens")

    def test_user_page_page_no_login(self):
        response = self.client.get('/user_page/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'under_construction.html')
        self.assertContains(response, "This site is under construction")
        self.assertNotContains(response, "Ancient Athens")

    def test_update_post_page_no_login(self):
        response = self.client.get('/update_post/introduction/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'under_construction.html')
        self.assertContains(response, "This site is under construction")
        self.assertNotContains(response, "Ancient Athens")

    def test_nonexistent_page_no_login(self):
        response = self.client.get('/sdkfj/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'under_construction.html')
        self.assertContains(response, "This site is under construction")
        self.assertNotContains(response, "Ancient Athens")

    # The one page that SHOULD be available without a login...
    def test_login_page_no_login(self):
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, "Log In")
        self.assertNotContains(response, "Ancient Athens")
