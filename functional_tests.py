from selenium import webdriver
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
        self.fail("finish me!")

if __name__ == '__main__':
    unittest.main(warnings='ignore')
