from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
import time

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        optionbox = self.browser.find_element_by_id('id_menu')
        self.assertAlmostEqual(
            optionbox.location['x'] + optionbox.size['width'] / 2,
            512,
            delta=10
        )

    #user can sort by column
    def test_column_sorting_date_ascending(self):
        self.browser.get(self.live_server_url + '/conversions/index')
        date_sort = self.browser.find_element_by_id('sort_date_asc')
        response = date_sort.click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, self.live_server_url + '/conversions/index?order_by=TimeExecuted&direction=asc'))

    def test_column_sorting_date_descending(self):
        self.browser.get(self.live_server_url + '/conversions/index')
        date_sort = self.browser.find_element_by_id('sort_date_des')
        response = date_sort.click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, self.live_server_url + '/conversions/index?order_by=TimeExecuted&direction=des'))

    def test_column_sorting_name_ascending(self):
        self.browser.get(self.live_server_url + '/conversions/index')
        date_sort = self.browser.find_element_by_id('sort_name_asc')
        response = date_sort.click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, self.live_server_url + '/conversions/index?order_by=Name&direction=asc'))

    def test_column_sorting_name_descending(self):
        self.browser.get(self.live_server_url + '/conversions/index')
        date_sort = self.browser.find_element_by_id('sort_name_des')
        response = date_sort.click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, self.live_server_url + '/conversions/index?order_by=Name&direction=des'))
