from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = self.browser.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # retrieve homepage
        self.browser.get(self.live_server_url)

        # check the page title and header mention 'to-do' lists
        self.assertIn("To-Do", self.browser.title)
        self.header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", self.header_text)

        # invited to enter a todo item right away
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
        )

        # type 'Buy peacock feathers' into a text box
        inputbox.send_keys("Buy peacock feathers")

        # When hitting enter the page updates to list "1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # can enter another item into text box
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # page updates and shows both items on list
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        self.fail("Finish the test!")

if __name__ == "__main__":
    unittest.main(warnings="ignore")
