# ccewredirect

Redirect from urls like `/charity/123456` to the appropriate page on the Charity Commission website

Example:

<https://ccew.dkane.net/charity/221603> -> <https://register-of-charities.charitycommission.gov.uk/charity-details/?regId=221603&subId=0>

## Scottish charities

If you enter a Scottish charity number it will redirect to their page on the OSCR website:

<https://ccew.dkane.net/charity/SC042837> -> <https://www.oscr.org.uk/about-charities/search-the-register/charity-details?number=SC042837>

## Accounts

For charities in England and Wales, you can link to their charity accounts using an url like `/charity/123456/accounts/2020-03-31`. The financial year end must be in `YYYY-MM-DD` format. If the account isn't found it will return a 404, otherwise it will redirect to the PDF accounts.

Example:

<https://ccew.dkane.net/charity/221603/accounts/2018-12-31> -> Download PDF

## Launch tweet

<https://twitter.com/kanedr/status/1304342443417112576>
