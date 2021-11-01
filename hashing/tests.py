from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from .forms import HashForm
from .models import Hash
from django.core.exceptions import ValidationError
import hashlib
import time


class FunctionalTestCase(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_check_home_page(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Enter hash here:', self.browser.page_source)

    def test_hash_of_hello(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element(by=By.ID, value='id_text')
        text.send_keys('hello')
        self.browser.find_element(by=By.NAME, value='submit').click()
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', self.browser.page_source)

    def test_hash_ajax(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element(by=By.ID, value='id_text')
        text.send_keys('hello')
        time.sleep(5)  # wait for AJAX
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', self.browser.page_source)

    def tearDown(self):
        self.browser.quit()


class UnitTestCase(TestCase):

    def test_home_page_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hashing/home.html')

    def test_hash_form(self):
        form = HashForm(data={
            'text': 'hello'
        })

        self.assertTrue(form.is_valid())

    def test_hash_function_works(self):
        text_hash = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual('2CF24DBA5FB0A30E26E83B2AC5B9E29E1B161E5C1FA7425E73043362938B9824', text_hash.upper())

    @staticmethod
    def save_hash():
        _hash = Hash()
        _hash.text = 'hello'
        _hash.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        _hash.save()
        return _hash

    def test_hash_object(self):
        _hash = self.save_hash()
        pulled_hash = Hash.objects.get(hash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertEqual(pulled_hash.text, _hash.text)

    def test_viewing_hash(self):
        _hash = self.save_hash()
        response = self.client.get('/hash/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertContains(response, 'hello')

    def test_bad_data(self):
        def bad_hash():
            hash = Hash()
            hash.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824ggggg'
            hash.full_clean()

        self.assertRaises(ValidationError, bad_hash)
