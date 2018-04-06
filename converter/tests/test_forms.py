from django.test import TestCase
from converter.forms import ConversionForm

class ConversionFormTest(TestCase):

    def test_form_name_input_has_placeholder_and_css(self):
        form = ConversionForm()
        self.assertIn('class="form-control input-lg"', form.as_p())
