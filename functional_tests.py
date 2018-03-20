from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_make_conversion_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        # User navigates to homepage and sees correct title
        self.assertIn('Batchcave', self.browser.title)

        # user is presented with options for creating a new conversion or
        # viewing past conversions
        select_menu = self.browser.find_element_by_id('id_create_new')
        self.assertEqual(
            select_menu.get_attribute('placeholder'),
            'Create New Conversion'
        )

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('BatchCave', header_text)

        #User can choose to start a new conversion
        first_choice = self.browser.find_element_by_id('id_menu_createConversion')
        self.assertIn('Create New Conversion', first_choice.text)
        #User can view an index of past conversions
        second_choice = self.browser.find_element_by_id('id_menu_indexConversion')
        self.assertIn('View Past Conversions', second_choice.text)
        self.fail("finish me!")

if __name__ == '__main__':
    unittest.main(warnings='ignore')
