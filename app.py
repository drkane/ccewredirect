import datetime

import mechanicalsoup
from flask import Flask, abort, redirect, request

app = Flask(__name__)
browser = mechanicalsoup.StatefulBrowser()
CCEW_URL = "https://register-of-charities.charitycommission.gov.uk/"
OSCR_URL = "https://www.oscr.org.uk/"
FTC_URL = "https://findthatcharity.uk/"


def get_charity_url(regno: str):
    if regno.startswith("SC"):
        return (
            OSCR_URL
            + "about-charities/search-the-register/charity-details?number={}".format(
                regno
            )
        )
    else:
        return CCEW_URL + "charity-details/?regId={}&subId=0".format(regno)


class StripLinkText(str):
    def __eq__(self, other):
        return self.strip() == other.strip()


@app.route("/")
def homepage():
    return redirect(FTC_URL, code=303)


@app.route("/charity/<regno>")
def charity(regno: str):
    redirect_url = get_charity_url(regno)
    return redirect(redirect_url, code=303)


@app.route("/charity/<regno>/accounts/<fyend>")
def accounts(regno: str, fyend: str):
    user_agent = request.headers.get("User-Agent")
    try:
        fyend = datetime.datetime.strptime(fyend, "%Y-%m-%d")
    except ValueError as e:
        abort(400, description=str(e))
    charity_url = get_charity_url(regno)
    if charity_url.startswith(CCEW_URL):
        browser.open(charity_url, headers={"User-Agent": user_agent})
        try:
            browser.follow_link(
                link_text=StripLinkText("Accounts and annual returns"),
                requests_kwargs=dict(
                    headers={"User-Agent": user_agent},
                ),
            )
        except mechanicalsoup.utils.LinkNotFoundError:
            abort(404, description="No accounts available for this charity")
        for tr in browser.get_current_page().find_all("tr", class_="govuk-table__row"):
            cells = list(tr.find_all("td"))
            if (
                cells
                and (cells[0].string.strip().lower() == "accounts and tar")
                and (cells[1].text[:30].strip() == fyend.strftime("%d %B %Y"))
            ):
                return redirect(tr.find("a").attrs["href"], code=303)
        abort(404, description="This account could be found for this charity")
    abort(404, description="Cannot access accounts for this charity")
