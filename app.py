from flask import Flask, redirect
import mechanicalsoup
import requests

app = Flask(__name__)
browser = mechanicalsoup.StatefulBrowser()
CCEW_URL = 'https://register-of-charities.charitycommission.gov.uk/'

@app.route('/')
def homepage():
    return redirect(CCEW_URL, code=303)

@app.route('/charity/<regno>')
def charity(regno):
    if regno.startswith("SC"):
        redirect_url = "https://www.oscr.org.uk/about-charities/search-the-register/charity-details?number={}".format(regno)
    else:
        redirect_url = CCEW_URL + "charity-details/?regId={}&subId=0".format(regno)
    return redirect(redirect_url, code=303)
