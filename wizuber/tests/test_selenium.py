import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from wizuber.models import Customer, Wizard, Student, Spirit, SpiritGrades

WIZARD_START_BALANCE = 13
PASSWORD = '123'


@tag('selenium')
class SeleniumBusinessCaseTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if 'MOSE_TEST_SELENIUM_HEADLESS' in os.environ:
            options = Options()
            options.headless = True
        else:
            options = None
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)

    def setUp(self) -> None:
        super().setUp()
        self.customer = Customer.objects.create_user('test_customer', 'customer@test.com', PASSWORD)
        self.wizard = Wizard.objects.create_user('test_wizard', 'wizard@test.com', PASSWORD,
                                                 balance=WIZARD_START_BALANCE)
        self.student = Student.objects.create_user('test_student', 'student@test.com', PASSWORD, teacher=self.wizard)
        self.spirit = Spirit.objects.create_user('test_spirit', 'spirit@test.com', PASSWORD,
                                                 grade=SpiritGrades.FOLIOT.name)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.close()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/wizuber/account/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(self.customer.username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(PASSWORD)
        self.selenium.find_element_by_xpath("//button[@type='submit']").click()
        create_wish_btn = self.selenium.find_element_by_css_selector('.btn-outline-success')
        self.assertEqual(create_wish_btn.text, 'Create New Wish!')
