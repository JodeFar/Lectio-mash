import requests
from bs4 import BeautifulSoup
from skole_ider import fo_skole_id

print(
        "hvis der er flere skoler med samme fornavn som din skole bliver du nødt til at skrive hele nanvet på din skole fx:\nFrederikshavn Gymnasium \nFrederikshavn Handelsskole \ndeler navn for at skelne melle de to institutioner gives det fulde navn\n\n")
skole_id = fo_skole_id(input("din skoles navn: "))

def get_headers_and_cookies(username, password):
    cookies = {
        'lectiogsc': '7c7a6d1c-2441-d8da-bf27-961598f3a500',
        'LastLoginExamno': skole_id,
        'BaseSchoolUrl': '754',
        'LastAuthenticatedPageLoad': 'Sun%21Feb%2018%202023%2020:11:50%20GMT+0100%20(Centraleurop%C3%A6isk%20normaltid)',
        'autologinkey': '12345678912UFdj132420',
        'isloggedin3': 'N',
    }
    headers = {
        'authority': 'www.lectio.dk',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'origin': 'https://www.lectio.dk',
        'referer': f'https://www.lectio.dk/lectio/{skole_id}/login.aspx?prevurl=forside.aspx',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 RuxitSynthetic/1.0 v7193743637908006844 t6526192659551348816 ath2653ab72 altpriv cvcv=2 smf=0',
    }
    params = {
        'prevurl': 'forside.aspx',
    }

    # Set the URL of the login page
    url = f'https://www.lectio.dk/lectio/{skole_id}/login.aspx'
    session = requests.Session()

    # Get the initial login page to obtain the ViewState and EventValidation values and ASP.net session value
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    cookies["ASP.NET_SessionId"] = response.cookies["ASP.NET_SessionId"] #tilføjer til cookies ASP.NET....
    viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
    eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

    data = {
        'time': '0',
        '__EVENTTARGET': 'm$Content$submitbtn2',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__SCROLLPOSITION': '',
        '__VIEWSTATEX': viewstate,
        '__VIEWSTATEY_KEY': '',
        '__VIEWSTATE': '',
        '__EVENTVALIDATION': eventvalidation,
        'm$Content$username': username,
        'm$Content$password':  password,
        'm$Content$AutologinCbx': 'on',
        'masterfootervalue': 'X1!ÆØÅ',
        'LectioPostbackId': '',
    }

    response = requests.post(f'https://www.lectio.dk/lectio/{skole_id}/login.aspx', params=params, cookies=cookies, headers=headers, data=data, allow_redirects=False)
    try:
        cookies[ 'autologinkey'] = response.cookies['autologinkey']
        cookies["isloggedin3"] = "Y"
        print("fik fanget alle de nødvendige headers og cookies")
    except:
        print("kunne ikke skabe autologinkey eller  ASP.NET_SessionId: skyldes nok at koden eller brugernavnet er skrevet forkert")
        print(response.cookies)

    response.close()
    return headers, cookies



