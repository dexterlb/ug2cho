import requests
import re
import dataclasses
import http.cookiejar

@dataclasses.dataclass
class URL:
    url: str

    _is_url = re.compile(r"^https?://", re.IGNORECASE)

    @classmethod
    def parse(cls, s: str):
        if cls._is_url.match(s):
            return cls(url=s)

def download(url, cookies_file=None):
    if cookies_file:
        cookiejar = http.cookiejar.MozillaCookieJar(cookies_file)
        cookiejar.load(ignore_expires=True, ignore_discard=True)
    else:
        cookiejar = requests.cookies.RequestsCookieJar()

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
    }

    return requests.get(url.url, headers=headers, cookies=cookiejar)
