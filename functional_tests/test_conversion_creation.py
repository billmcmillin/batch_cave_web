from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):


    def test_can_view_menu(self):
        self.browser.get(self.live_server_url)

        # User navigates to homepage and sees correct title
        self.assertIn('BatchCave', self.browser.title)

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

