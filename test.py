import string
import unittest
from main import *


class TestCrawlyScrapper(unittest.TestCase):
    def test_replace_token(self):
        reversed_ascii = string.ascii_lowercase[::-1]
        reversed_digits = string.digits[::-1]
        self.assertEqual(reversed_ascii, replace_token(string.ascii_lowercase))
        self.assertEqual(reversed_digits, replace_token(string.digits))

    def test_extract_token(self):
        home_page_html = """
        <html>
        <head>
            <script src="adpagespeed.js"></script>
        </head>
        <body>
        <form action="/" method="post" id="form">
            <input type="hidden" name="token" id="token" value="y70w7uy1yv2w41442u10z5y2uv042v39" />
            <input type="button" value="Descobrir resposta" onClick="findAnswer()">
        </form>
        </body>
        </html>
        """
        token = extract_token(home_page_html)
        self.assertEqual(token, "y70w7uy1yv2w41442u10z5y2uv042v39")

    def test_extract_cookie(self):
        headers = {"Set-Cookie": "PHPSESSID=pe8u5gi5fomrmrnasm9vbbrme0; path=/"}
        cookie = extract_cookie(headers)
        self.assertEqual(cookie, "PHPSESSID=pe8u5gi5fomrmrnasm9vbbrme0")

    def test_extract_response_number(self):
        response_page_html = """
        RESPOSTA: <span id="answer">93</span><br /><a href="http://applicant-test.us-east-1.elasticbeanstalk.com/">Voltar</a>
        """
        response_number = extract_response_number(response_page_html)
        self.assertEqual(response_number, "93")


if __name__ == "__main__":
    unittest.main()
