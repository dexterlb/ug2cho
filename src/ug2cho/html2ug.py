from bs4 import BeautifulSoup
import json

from ug2cho.ug import UG

def html2ug(html_text: str) -> UG:
    bs = BeautifulSoup(html_text, 'html.parser')
    data = bs.find("div", {"class": "js-store"})
    data = data.attrs['data-content']
    data = json.loads(data)

    raw_leadsheet = data["store"]["page"]["data"]["tab_view"]["wiki_tab"]["content"]
    leadsheet = raw_leadsheet.replace('\r\n', '\n').strip() + '\n'

    metadata = {
        'artist_name': data["store"]["page"]["data"]["tab"]['artist_name'],
        'key': data["store"]["page"]["data"]["tab"].get('tonality_name'),
        'song_name': data["store"]["page"]["data"]["tab"]["song_name"],
        'version': int(data["store"]["page"]["data"]["tab"]["version"]),
        'type': data["store"]["page"]["data"]["tab"]["type"],
        'rating': int(data["store"]["page"]["data"]["tab"]["rating"]),
        'difficulty': data["store"]["page"]["data"]["tab_view"]["ug_difficulty"],
        'applicature': data["store"]["page"]["data"]["tab_view"]["applicature"],
        'leadsheet_url': data["store"]["page"]["data"]["tab"]["tab_url"],
        'leadsheet_author': data['store']['page']['data']['tab']['username'],
    }

    metadata['leadsheet_author_url'] = f'https://www.ultimate-guitar.com/u/{metadata['leadsheet_author']}'

    if type(data["store"]["page"]["data"]["tab_view"]["meta"]) is dict:
        metadata['capo'] = data["store"]["page"]["data"]["tab_view"]["meta"].get("capo")
        _tuning = data["store"]["page"]["data"]["tab_view"]["meta"].get("tuning")
        metadata['tuning'] = f"{_tuning['value']} ({_tuning['name']})" if _tuning else None

    metadata = {k: v for k, v in metadata.items() if v}

    return UG(leadsheet=leadsheet, metadata=metadata)
