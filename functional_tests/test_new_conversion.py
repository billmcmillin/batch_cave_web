from .base import FunctionalTest
from selenium import webdriver
from unittest import skip
from selenium.webdriver.common.keys import Keys
import time
from django.test.utils import override_settings
from selenium.webdriver.support.ui import Select

class NewConversionTest(FunctionalTest):
    def test_user_enters_conversion_info(self):
        self.browser.get(self.live_server_url + '/conversions/create/')
        select = Select(self.browser.find_element_by_tag_name("select"))
        select.select_by_visible_text("ER_EAI_2nd")
        #User selects a process
        nameBox = self.get_name_input_box()
        nameBox.send_keys('Firstiest conversion')

        #User is able to upload a file through dialog box
        uploadBox = self.browser.find_element_by_id("id_Upload")
        uploadBox.send_keys("~/TEST.mrc")
        submitButton = self.browser.find_element_by_tag_name("form")
        submitButton.submit()

        #user sees a list of past conversions
        self.wait_for_row_in_list_table('Firstiest conversion')

        #user sees the type of conversion selected
        self.wait_for_row_in_list_table('ER_EAI_2nd')
