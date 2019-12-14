import os
from contextlib import contextmanager
from typing import List, Collection

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from django.urls import reverse
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

from wizuber.models import Customer, Wizard, Student, Spirit, SpiritGrades, Wish, WishStatus

WIZARD_START_BALANCE = 13
CUSTOMER_START_BALANCE = 322
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
        self.customer = Customer.objects.create_user('test_customer', 'customer@test.com', PASSWORD,
                                                     balance=CUSTOMER_START_BALANCE)
        self.wizard = Wizard.objects.create_user('test_wizard', 'wizard@test.com', PASSWORD,
                                                 balance=WIZARD_START_BALANCE)
        self.student = Student.objects.create_user('test_student', 'student@test.com', PASSWORD, teacher=self.wizard)
        self.spirit = Spirit.objects.create_user('test_spirit', 'spirit@test.com', PASSWORD,
                                                 grade=SpiritGrades.FOLIOT.name)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.close()
        super().tearDownClass()

    def refresh(self):
        self.customer.refresh_from_db()
        self.wizard.refresh_from_db()
        self.student.refresh_from_db()
        self.spirit.refresh_from_db()
        if self.wish is not None:
            self.wish.refresh_from_db()

    @contextmanager
    def wait_for_page_load(self, timeout=10):
        """ http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html """
        old_page = self.selenium.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.selenium, timeout).until(staleness_of(old_page))

    def url(self, postfix: str) -> str:
        """ Usage: self.url(reverse('wizuber:list-with')) """
        return f'{self.live_server_url}{postfix}'

    def reverse_for_action(self, action_name: str) -> str:
        kwargs = dict(pk=self.wish.pk, action=action_name)
        return reverse('wizuber:handle-wish-action', kwargs=kwargs)

    def check_form_actions(self, forms: List[WebElement], action_names: Collection[str]) -> None:
        self.assertEqual(len(forms), len(action_names))
        expected_actions = set(
            self.url(self.reverse_for_action(name))
            for name in action_names
        )
        form_actions = set(form.get_attribute('action') for form in forms)
        self.assertEqual(expected_actions, form_actions)

    def find_form_by_name(self, action_name: str) -> WebElement:
        action = self.reverse_for_action(action_name)
        return self.selenium.find_element_by_css_selector(f"form[action='{action}']")

    def find_all_forms(self) -> List[WebElement]:
        return self.selenium.find_elements_by_tag_name('form')

    def test_business_scenario_selenium(self):
        self.selenium.get(self.url(reverse('wizuber:login')))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(self.customer.username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(PASSWORD)
        with self.wait_for_page_load():
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
        self.wish = Wish.objects.first()
        self.assertEqual(self.wish.description, 'test description\r\nwith linebreak')
        self.assertEqual(self.wish.price, 42)
        self.assertEqual(self.wish.status, WishStatus.NEW.name)

        self.check_form_actions(self.find_all_forms(), ['delete', 'pay'])

        pay_form = self.find_form_by_name('pay')
        pay_btn = pay_form.find_element_by_css_selector('button[type="submit"]')
        self.assertEqual(pay_btn.text, 'Pay for wish')
        with self.wait_for_page_load():
            pay_btn.submit()

        self.refresh()
        self.assertTrue(self.wish.in_status(WishStatus.ACTIVE))
        self.assertEqual(self.customer.balance, CUSTOMER_START_BALANCE - self.wish.price)
        self.check_form_actions(self.find_all_forms(), [])
