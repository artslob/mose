import os
from contextlib import contextmanager
from typing import List, Iterable

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from django.urls import reverse
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from wizuber.fsm import action_names as possible_action_names
from wizuber.models import (
    Customer,
    Wizard,
    Student,
    Spirit,
    SpiritGrades,
    Wish,
    WishStatus,
    CandleMaterial,
    SizeChoices,
)

WIZARD_START_BALANCE = 13
CUSTOMER_START_BALANCE = 322
PASSWORD = "123"


@tag("selenium")
class SeleniumBusinessCaseTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if "MOSE_TEST_SELENIUM_HEADLESS" in os.environ:
            options = Options()
            options.headless = True
        else:
            options = None
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)

    def setUp(self) -> None:
        super().setUp()
        self.customer = Customer.objects.create_user(
            "test_customer",
            "customer@test.com",
            PASSWORD,
            balance=CUSTOMER_START_BALANCE,
        )
        self.wizard = Wizard.objects.create_user(
            "test_wizard", "wizard@test.com", PASSWORD, balance=WIZARD_START_BALANCE
        )
        self.student = Student.objects.create_user(
            "test_student", "student@test.com", PASSWORD, teacher=self.wizard
        )
        self.spirit = Spirit.objects.create_user(
            "test_spirit", "spirit@test.com", PASSWORD, grade=SpiritGrades.FOLIOT.name
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.close()
        super().tearDownClass()

    # helper methods

    def refresh(self):
        self.customer.refresh_from_db()
        self.wizard.refresh_from_db()
        self.student.refresh_from_db()
        self.spirit.refresh_from_db()
        if self.wish is not None:
            self.wish.refresh_from_db()

    @contextmanager
    def wait_for_page_load(self, timeout=10):
        """ http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html """  # noqa: E501
        old_page = self.selenium.find_element_by_tag_name("html")
        yield
        WebDriverWait(self.selenium, timeout).until(staleness_of(old_page))

    def url(self, postfix: str) -> str:
        """ Usage: self.url(reverse('wizuber:list-with')) """
        return f"{self.live_server_url}{postfix}"

    def reverse_for_action(self, action_name: str) -> str:
        kwargs = dict(pk=self.wish.pk, action=action_name)
        return reverse("wizuber:handle-wish-action", kwargs=kwargs)

    def check_available_actions(self, action_names: Iterable[str]) -> None:
        action_forms = [
            form
            for form in self.find_all_forms()
            if form.get_attribute("name") in possible_action_names()
        ]
        expected_actions = set(
            self.url(self.reverse_for_action(name)) for name in action_names
        )
        form_actions = set(form.get_attribute("action") for form in action_forms)
        self.assertEqual(expected_actions, form_actions)

    def find_form_by_name(self, action_name: str) -> WebElement:
        action = self.reverse_for_action(action_name)
        return self.selenium.find_element_by_css_selector(f"form[action='{action}']")

    def find_all_forms(self) -> List[WebElement]:
        return self.selenium.find_elements_by_tag_name("form")

    def login_as(self, user_model):
        self.selenium.get(self.url(reverse("wizuber:login")))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(user_model.username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(PASSWORD)
        with self.wait_for_page_load():
            self.selenium.find_element_by_xpath("//button[@type='submit']").click()

    def go_to_wish_page(self):
        wish_detail = reverse("wizuber:detail-wish", kwargs=dict(pk=self.wish.pk))
        self.selenium.get(self.url(wish_detail))

    def submit(self, form):
        with self.wait_for_page_load():
            form.submit()

    # test of primary business scenario

    def test_business_scenario_selenium(self):
        self.login_as(self.customer)

        create_wish_btn = self.selenium.find_element_by_css_selector(
            ".btn-outline-success"
        )
        self.assertEqual(create_wish_btn.text, "Create New Wish!")

        with self.wait_for_page_load():
            create_wish_btn.click()

        self.assertEqual(Wish.objects.count(), 0)

        wish_description = self.selenium.find_element_by_name("description")
        wish_description.send_keys("test description\nwith linebreak")

        wish_price = self.selenium.find_element_by_name("price")
        wish_price.clear()
        wish_price.send_keys("42")

        self.submit(wish_price)

        self.assertEqual(Wish.objects.count(), 1)
        self.wish = Wish.objects.first()
        self.assertEqual(self.wish.description, "test description\r\nwith linebreak")
        self.assertEqual(self.wish.price, 42)
        self.assertEqual(self.wish.status, WishStatus.NEW.name)

        self.check_available_actions(["delete", "pay"])

        pay_form = self.find_form_by_name("pay")
        pay_btn = pay_form.find_element_by_css_selector('button[type="submit"]')
        self.assertEqual(pay_btn.text, "Pay for wish")
        self.submit(pay_btn)

        self.refresh()
        self.assertTrue(self.wish.in_status(WishStatus.ACTIVE))
        self.assertEqual(
            self.customer.balance, CUSTOMER_START_BALANCE - self.wish.price
        )
        self.check_available_actions([])

        self.wizard_own_wish()

        self.candle_artifact_creation()

        self.assign_to_student()

        self.login_as(self.student)
        self.go_to_wish_page()

        self.check_available_actions(
            ["to-wizard", "spirit-artifact", "candle-artifact", "pentacle-artifact"]
        )
        self.check_pentacle_artifact_creation()
        self.check_available_actions(
            ["to-wizard", "spirit-artifact", "candle-artifact", "pentacle-artifact"]
        )

        self.check_spirit_artifact_creation()
        self.check_available_actions(
            ["to-wizard", "spirit-artifact", "candle-artifact", "pentacle-artifact"]
        )

        self.check_assign_to_wizard()
        self.check_available_actions([])

        self.login_as(self.wizard)
        self.go_to_wish_page()
        self.check_available_actions(
            [
                "spirit-artifact",
                "candle-artifact",
                "pentacle-artifact",
                "to-student",
                "to-spirit",
            ]
        )

        self.check_assign_to_spirit()
        self.check_available_actions([])

        self.login_as(self.spirit)
        self.go_to_wish_page()
        self.check_available_actions(["spirit-to-wizard"])

        self.check_assign_from_spirit_to_wizard()

        self.login_as(self.wizard)
        self.go_to_wish_page()
        self.check_available_actions(["close"])
        self.assertEqual(self.wizard.balance, WIZARD_START_BALANCE)

        self.check_close_action()
        self.check_available_actions([])

    # tests component parts

    def wizard_own_wish(self):
        self.login_as(self.wizard)
        self.go_to_wish_page()
        self.check_available_actions(["own"])

        own_form = self.find_form_by_name("own")
        own_btn = own_form.find_element_by_css_selector('button[type="submit"]')
        self.assertEqual(own_btn.text, "Take ownership")
        self.submit(own_btn)

        self.refresh()
        self.assertTrue(self.wish.in_status(WishStatus.WORK))
        self.assertTrue(self.wish.owner == self.wish.assigned_to == self.wizard)
        self.assertEqual(self.wizard.owned_wishes.count(), 1)
        self.assertEqual(self.wish.pentacle_artifacts.count(), 0)
        self.assertEqual(self.wish.candle_artifacts.count(), 0)
        self.assertFalse(self.wish.has_spirit_artifact())
        self.check_available_actions(
            ["spirit-artifact", "candle-artifact", "pentacle-artifact", "to-student"]
        )

    def candle_artifact_creation(self):
        candle_artifact_form = self.find_form_by_name("candle-artifact")

        size_select = Select(candle_artifact_form.find_element_by_name("size"))
        size_select.select_by_value(SizeChoices.SMALL.name)

        material_select = Select(candle_artifact_form.find_element_by_name("material"))
        material_select.select_by_value(CandleMaterial.TALLOW.name)

        self.submit(candle_artifact_form)

        self.refresh()
        self.assertEqual(self.wish.candle_artifacts.count(), 1)
        candle = self.wish.candle_artifacts.first()
        self.assertEqual(candle.wish, self.wish)
        self.assertEqual(candle.material, CandleMaterial.TALLOW.name)
        self.assertEqual(candle.size, SizeChoices.SMALL.name)

    def assign_to_student(self):
        to_student_form = self.find_form_by_name("to-student")
        self.submit(to_student_form)

        self.refresh()
        self.assertTrue(self.wish.owner == self.wizard)
        self.assertTrue(self.wish.assigned_to == self.student)

    def check_pentacle_artifact_creation(self):
        pentacle_artifact_form = self.find_form_by_name("pentacle-artifact")

        name = pentacle_artifact_form.find_element_by_name("name")
        name.send_keys("some test pentacle")

        size_select = Select(pentacle_artifact_form.find_element_by_name("size"))
        size_select.select_by_value(SizeChoices.LARGE.name)

        self.submit(pentacle_artifact_form)

        self.refresh()
        self.assertEqual(self.wish.pentacle_artifacts.count(), 1)
        pentacle = self.wish.pentacle_artifacts.first()
        self.assertEqual(pentacle.wish, self.wish)
        self.assertEqual(pentacle.name, "some test pentacle")
        self.assertEqual(pentacle.size, SizeChoices.LARGE.name)

    def check_spirit_artifact_creation(self):
        spirit_artifact_form = self.find_form_by_name("spirit-artifact")

        spirit_select = Select(spirit_artifact_form.find_element_by_name("spirit"))
        spirit_select.select_by_value(str(self.spirit.pk))

        self.submit(spirit_artifact_form)

        self.refresh()
        self.assertTrue(self.wish.has_spirit_artifact())
        self.assertEqual(self.wish.spirit_artifact.wish, self.wish)
        self.assertEqual(self.wish.spirit_artifact.spirit, self.spirit)

    def check_assign_to_wizard(self):
        to_wizard_form = self.find_form_by_name("to-wizard")
        self.submit(to_wizard_form)

        self.refresh()
        self.assertTrue(self.wish.owner == self.wizard)
        self.assertTrue(self.wish.assigned_to == self.wizard)

    def check_assign_to_spirit(self):
        to_spirit_form = self.find_form_by_name("to-spirit")
        self.submit(to_spirit_form)

        self.refresh()
        self.assertTrue(self.wish.in_status(WishStatus.ON_SPIRIT))
        self.assertEqual(self.wish.owner, self.wizard)
        self.assertEqual(self.wish.assigned_to, self.spirit)

    def check_assign_from_spirit_to_wizard(self):
        spirit_to_wizard_form = self.find_form_by_name("spirit-to-wizard")
        self.submit(spirit_to_wizard_form)

        self.refresh()
        self.assertTrue(self.wish.in_status(WishStatus.READY))
        self.assertTrue(self.wish.owner == self.wish.assigned_to == self.wizard)

    def check_close_action(self):
        close_form = self.find_form_by_name("close")
        self.submit(close_form)

        self.refresh()
        self.assertTrue(self.wish.in_status(WishStatus.CLOSED))
        self.assertTrue(self.wish.owner == self.wizard)
        self.assertTrue(self.wish.creator == self.wish.assigned_to == self.customer)
        self.assertEqual(self.wizard.balance, WIZARD_START_BALANCE + self.wish.price)
