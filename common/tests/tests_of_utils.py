import re

from django.test import TestCase

from common.utils import gen_mobile_code, gen_captcha_text


class TestOfUtils(TestCase):

    def test_gen_mobile_code(self):
        pattern = re.compile(r'\d{6}')
        for _ in range(10000):
            self.assertRegex(gen_mobile_code(), pattern)

    def test_gen_captcha_text(self):
        pattern = re.compile(r'[0-9a-zA-Z]{4}')
        for _ in range(10000):
            self.assertRegex(gen_captcha_text(), pattern)
