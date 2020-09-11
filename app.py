from flask import Flask, redirect
import mechanicalsoup
import requests

app = Flask(__name__)
browser = mechanicalsoup.StatefulBrowser()
CCEW_URL = 'https://register-of-charities.charitycommission.gov.uk/'

@app.route('/')
def homepage():
    response = browser.open(CCEW_URL)
    return response.content

@app.route('/charity/<regno>')
def charity(regno):
    browser.open(CCEW_URL + "charity-search")
    browser.select_form('#_uk_gov_ccew_portlet_CharitySearchPortlet_fm')
    browser.get_current_form().print_summary()
    browser['_uk_gov_ccew_portlet_CharitySearchPortlet_keywords'] = regno
    browser.submit_selected()
    response = browser.find_link(link_text=regno)
    return redirect(response['href'], code=303)
