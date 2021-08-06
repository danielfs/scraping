import json
import logging
import os
import re
import requests

from distutils.util import strtobool

URL = "http://applicant-test.us-east-1.elasticbeanstalk.com/"
REGEX_TOKEN = "[a-z0-9]{32}"
REGEX_RESPONSE = "\d+"
DEBUG = strtobool(os.environ.get("DEBUG", "false"))

if DEBUG:
    logging.basicConfig(format="%(message)s", level=logging.INFO)


def load_replacements_lookup():
    logging.info("Loading replacements lookup")
    with open("replacements_lookup.json", "r") as lookup_file:
        return json.loads(lookup_file.read())


def replace_token(token: str) -> str:
    logging.info(f"Replacing token {token}")
    replacements = load_replacements_lookup()
    new_token = ""
    for c in token:
        new_token += replacements[c]
    logging.info(f"New token {new_token}")
    return new_token


def get_home_page() -> requests.Response:
    logging.info("Getting Home Page")
    return requests.get(URL)


def extract_token(response_body: str) -> str:
    m = re.search(REGEX_TOKEN, response_body)
    token = m.group(0)
    logging.info(f"Token found {token}")
    return token


def extract_cookie(response_headers: str) -> str:
    cookie = response_headers.get("Set-Cookie").split(";")[0]
    logging.info(f"Cookie found {cookie}")
    return cookie


def get_response(cookie: str, new_token: str) -> str:
    logging.info("Getting response")
    headers = {
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Accept-Encoding": "gzip, deflate",
        "Origin": "http://applicant-test.us-east-1.elasticbeanstalk.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "http://applicant-test.us-east-1.elasticbeanstalk.com/",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": cookie,
    }
    response_page = requests.post(URL, data=f"token={new_token}", headers=headers)
    return response_page.text


def extract_response_number(response_body: str) -> str:
    logging.info(f"Extracting response number from {response_body}")
    m = re.search(REGEX_RESPONSE, response_body)
    response_number = m.group(0)
    return response_number


if __name__ == "__main__":
    load_replacements_lookup()
    home_page = get_home_page()
    cookie = extract_cookie(home_page.headers)
    token = extract_token(home_page.text)
    new_token = replace_token(token)
    response = get_response(cookie, new_token)
    response_number = extract_response_number(response)
    print(f"Response number found {response_number}")
