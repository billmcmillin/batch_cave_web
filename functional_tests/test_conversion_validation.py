from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.support.ui import Select

class ConversionValidationTest(FunctionalTest):

    def test_cannot_add_unnamed_conversion(self):
        #user enters all data except conversion name
        self.browser.get(self.live_server_url + '/conversions/create/')
        #User selects a process
        select = Select(self.browser.find_element_by_tag_name("select"))
        select.select_by_visible_text("ER_EAI_2nd")

        #User is able to upload a file through dialog box
        uploadBox = self.browser.find_element_by_id("id_Upload")
        uploadBox.send_keys("~/TEST.mrc")
        submitButton = self.browser.find_element_by_tag_name("form")
        submitButton.submit()

        #Error message is displayed
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "Conversion must have a name"
        ))
