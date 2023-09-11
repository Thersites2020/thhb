# To NOT run Selenium tests, use --exclude-tag=selenium

from django.test import TestCase, LiveServerTestCase
from django.test import override_settings, tag

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
import PIL

import time


@tag('selenium')
@override_settings(ALLOWED_HOSTS=['*'])
class HomePageVisitTest(TestCase):

    def setUp(self):
        firefox_options = webdriver.FirefoxOptions()
       # firefox_options.add_argument('--headless')
        self.firefox = webdriver.Remote(
            command_executor='http://selenium_hub:4444/wd/hub',
            options=firefox_options
        )
        self.firefox.implicitly_wait(10)

        # Create artifical image for testing
        img = PIL.Image.new(mode="RGB", size=(200, 200))
        img.save("test.jpg")


    def tearDown(self):
        self.firefox.quit()


    def test_user_visits_home_page(self):
        start_time = time.time()
        # User visits home page
        self.firefox.get('http://app:8000')
        time.sleep(3)
        self.assertEquals(self.firefox.title, 'This Has Happened Before')

        # ... and gets the 'under construction' page
        bodyText = self.firefox.find_element(By.TAG_NAME, 'body').text
        self.assertFalse("Ancient Athens" in bodyText)
        self.assertTrue("This site is under construction" in bodyText)

        self.firefox.find_element(By.CLASS_NAME, "login-btn").click()

        # User is now on login page
        main_text = self.firefox.find_element(By.CLASS_NAME, "main-text")
        self.assertIn("Log In", main_text.text)

        # User enters text in Username input
        username = self.firefox.find_element(By.NAME, "username")
        password = self.firefox.find_element(By.NAME, "password")
        button = self.firefox.find_element(By.CLASS_NAME, "login-btn")

        username.send_keys('testuser')
        password.send_keys('testpass123')
        button.send_keys(Keys.ENTER)

        # ... and gets to home page
        subtitle = self.firefox.find_element(By.CLASS_NAME, 'header__subtitle')
        self.assertTrue("Ancient Athens" in subtitle.text)
        self.assertTrue("New Here?" in self.firefox.page_source)

        # User clicks on username at top right
        self.firefox.find_element(By.CLASS_NAME, "usernav__username").click()

        # User is now on user-page
        userpage_title = self.firefox.find_element(By.CLASS_NAME, 'userpage__title')
        self.assertTrue("user page for".lower() in userpage_title.text.lower())

        # User clicks on Create New Post button
        self.firefox.find_element(By.LINK_TEXT, 'Create New Post').click()

        # User enters text in create post fields
        title = self.firefox.find_element(By.NAME, "title")
        title.send_keys('A New Test Post')
        subtitle = self.firefox.find_element(By.NAME, "subtitle")
        subtitle.send_keys('This is a Test Subtitle')
        self.firefox.find_element(By.XPATH, "//input[@type='file']").send_keys("test.jpg")
        image_alt = self.firefox.find_element(By.NAME, "image_alt")
        image_alt.send_keys('A Test Image')

        # (a JS script is necessary for the TinyMCE text editor box)
        self.firefox.execute_script("tinyMCE.activeEditor.setContent('<p>Test Text</p> TinyMCE')")

        # User submits new post
        submit_button = self.firefox.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

        # User sees post content text
        #print(self.firefox.page_source)
        new_post_title = self.firefox.find_element(By.CLASS_NAME, 'article-top__title').text
        self.assertIn('A New Test Post', new_post_title)
        self.assertTrue("This is a Test Subtitle" in self.firefox.page_source)

        # User clicks on Logout button
        self.firefox.find_element(By.LINK_TEXT, 'Logout').click()

        # User is back at Under Construction page
        UCText = self.firefox.find_element(By.TAG_NAME, 'body').text
        self.assertFalse("Ancient Athens" in UCText)
        self.assertTrue("This site is under construction" in UCText)

        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total time for test_user_visits_home_page: {total_time // 60} minutes {round(total_time % 60, 2)} seconds")
