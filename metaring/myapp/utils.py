import requests


url_beginning = "https://api.checkwx.com/v2/metar/"
url_ending = "/?x-api-key=577510bbb0d848039e037a083960f99f"


def base_url(ICAO):
    final_url = url_beginning + ICAO + url_ending
    return final_url

def get_metar_from_icao(ICAO):
    url = base_url(ICAO)
    response = requests.get(url)
    
    if response.status_code== 200:
        airport_metar = response.json()
        return airport_metar
    else:
        return None