import requests
from django.core.cache import cache


url_beginning = "https://api.checkwx.com/v2/metar/"
url_ending = "/?x-api-key=577510bbb0d848039e037a083960f99f"


def base_url(icao):
    final_url = url_beginning + icao + url_ending
    return final_url

def url_decoded(icao):
    final_url = url_beginning + icao + "/decoded" + url_ending
    return final_url

def get_metar_from_icao(icao):

    icao = icao.upper()
    cache_key = f"metar_{icao}"
    cached_metar = cache.get(cache_key)
    if cached_metar:
        return cached_metar
    
    url = base_url(icao)
    response = requests.get(url)
    
    if response.status_code== 200:
        airport_json = response.json()
        airport_metar = airport_json['data']
        cache.set(cache_key, airport_metar, timeout=600)
        return airport_metar
    else:
        return None
    
def get_metar_decoded(icao):

    icao = icao.upper()
    cache_key = f"metar_{icao}"
    cached_metar = cache.get(cache_key)
    if cached_metar:
        return cached_metar
    
    url = url_decoded(icao)

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return None

        data = response.json().get("data", [])
        if not data:
            return None

        metar = data[0]

        cache.set(cache_key, metar, timeout=600)

        return {
            "icao": metar.get("icao"),
            "raw_text": metar.get("raw_text"),
            "observed": metar.get("report", {}).get("observed"),
            "flight_category": metar.get("flight_category"),
            "humidity": metar.get("humidity"),
            "colors": metar.get("colors"),
            "wind": metar.get("wind"),
            "visibility": metar.get("visibility"),
            "temperature": metar.get("temperature"),
            "dewpoint": metar.get("dewpoint"),
            "pressure": metar.get("pressure"),
            "clouds": metar.get("clouds", []),
            "conditions": metar.get("conditions", []),
            "windshear": metar.get("windshear", []),
            "remarks": metar.get("remarks", []),
            "trend": metar.get("trend"),
            "runway_state": metar.get("runway_state"),
            "runway_visual": metar.get("runway_visual"),

            "position": metar.get("position"),
        }

    except requests.RequestException:
        return None