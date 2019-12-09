import os
from contextlib import contextmanager

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

from wizuber.models import Customer, Wizard, Student, Spirit, SpiritGrades, Wish

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

    @contextmanager
    def wait_for_page_load(self, timeout=10):
        """ http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html """
        old_page = self.selenium.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.selenium, timeout).until(staleness_of(old_page))

    def test_business_scenario_selenium(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/wizuber/account/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(self.customer.username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(PASSWORD)
        self.selenium.find_element_by_xpath("//button[@type='submit']").click()
        create_wish_btn = self.selenium.find_element_by_css_selector('.btn-outline-success')
        self.assertEqual(create_wish_btn.text, 'Create New Wish!')

        with self.wait_for_page_load():
            create_wish_btn.click()

        self.assertEqual(Wish.objects.count(), 0)

        wish_description = self.selenium.find_element_by_name('description')
        wish_description.send_keys('test description\nwith linebreak')

        wish_price = self.selenium.find_element_by_name('price')
        wish_price.clear()
        wish_price.send_keys('42')

        with self.wait_for_page_load():
            wish_price.submit()

        self.assertEqual(Wish.objects.count(), 1)
        wish = Wish.objects.first()
        self.assertEqual(wish.description, 'test description\r\nwith linebreak')
        self.assertEqual(wish.price, 42)
