from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time




class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_make_conversion_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        # User navigates to homepage and sees correct title
        self.assertIn('Batchcave', self.browser.title)

        # user is presented with options for creating a new conversion or
        # viewing past conversions

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Batchcave', header_text)

        #User can choose to start a new conversion
        first_choice = self.browser.find_element_by_id('id_menu_createConversion')
        self.assertIn('Create New Conversion', first_choice.text)
        #User can view an index of past conversions
        second_choice = self.browser.find_element_by_id('id_menu_indexConversion')
        self.assertIn('View Past Conversions', second_choice.text)

class NewConversionTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_make_conversion_and_retrieve_it_later(self):
        # User navigates to new conversion page and sees correct title
        self.browser.get('http://localhost:8000/conversions/create')

        self.assertIn('Create New Conversion', self.browser.title)

        inputbox = self.browser.find_element_by_id("id_new_conversion")
        inputbox.send_keys('peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.browser.get('http://localhost:8000/conversions/create')
        #user enters a second item
        inputbox = self.browser.find_element_by_id('id_new_conversion')
        inputbox.send_keys('turtle feathers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #page updates and shows both conversion names entered
        self.check_for_row_in_list_table('peacock feathers')
        self.check_for_row_in_list_table('turtle feathers')

