from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

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
    def test_column_sorting(self):
        self.browser.get(self.live_server_url + '/index/')
        date_sort = self.browser.find_element_by_id('sort_date_asc')
