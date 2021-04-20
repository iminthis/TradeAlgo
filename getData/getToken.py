import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import urllib
import requests
from splinter import Browser
from secret.config import key, password, user_id

executeable_path = {'executable_path': r'C:\Users\Vinay\Desktop\tradealgo\chromedriver.exe'}

def getaccess():
    start = time.time()
    browser = Browser("chrome", **executeable_path, headless = False)

    method = "GET"
    url = "https://auth.tdameritrade.com/auth?"
    client_code = key + "@AMER.OAUTHAP"
    payload = {
        'response_type': 'code',
        'redirect_uri': "http://localhost",
        'client_id': client_code
    }

    built_url = requests.Request(method, url, params = payload).prepare()
    built_url = built_url.url

    browser.visit(built_url)

    payload = {
        'username': user_id,
        'password': password
    }

    browser.find_by_id("username0").first.fill(payload["username"])
    browser.find_by_id("password1").first.fill(payload["password"])
    browser.find_by_id("accept").first.click()

    browser.find_by_id("accept").first.click()
    time.sleep(1)

    browser.find_by_text('Can\'t get the text message?').first.click()

    # Get the Answer Box
    browser.find_by_value("Answer a security question").first.click()

    # Answer the Security Questions.
    if browser.is_text_present(''):
        browser.find_by_id("secretquestion0").first.click()
        browser.find_by_id('secretquestion0').first.fill('')

    elif browser.is_text_present(''):
        browser.find_by_id("secretquestion0").first.click()
        browser.find_by_id('secretquestion0').first.fill('')

    elif browser.is_text_present(''):
        browser.find_by_id("secretquestion0").first.click()
        browser.find_by_id('secretquestion0').first.fill('')

    elif browser.is_text_present(''):
        browser.find_by_id("secretquestion0").first.click()
        browser.find_by_id('secretquestion0').first.fill('')

    # Submit results
    browser.find_by_id('accept').first.click()

    #Trust this device
    browser.find_by_xpath('/html/body/form/main/fieldset/div/div[1]/label').first.click()
    browser.find_by_id('accept').first.click()
    browser.find_by_id('accept').first.click()

    new_url = browser.url

    parse_url = urllib.parse.unquote(new_url.split("code=")[1])

    url = "https://api.tdameritrade.com/v1/oauth2/token"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        'grant_type': 'authorization_code',
        'access_type': 'offline',
        'code': parse_url,
        'client_id': key,
        'redirect_uri': 'http://localhost'
    }

    authreply = requests.post(url, headers = headers, data = payload).json()
    #print(authreply)
    #print(json.dumps(authreply, indent = 4))

    try:
        access_token = authreply['access_token']
    except:
        access_token = authreply['access_token']

    f = open(r"C:\Users\Vinay\Desktop\tradealgo\getData\access_token.txt", "w")
    f.truncate(0)
    f.write(access_token)
    f.close()
    #print(access_token)

    browser.quit()

#getaccess()
