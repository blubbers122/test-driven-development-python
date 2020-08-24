from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        print(self.browser)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # retrieve homepage
        self.browser.get('http://localhost:8000')

        # check the page title and header mention 'to-do' lists
        self.assertIn("To-Do", self.browser.title)
        self.header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # invited to enter a todo item right away
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
        )



        self.fail("Finish the test!")

if __name__ == "__main__":
    unittest.main(warnings="ignore")
