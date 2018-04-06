from .base import FunctionalTest

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
