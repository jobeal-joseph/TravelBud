import requests

def search_cities(query):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "addressdetails": 1, "limit": 6}
    headers = {"User-Agent": "TravelBud_App"}
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        return [{"city": i.get("address", {}).get("city") or i.get("display_name").split(',')[0],
                 "country": i.get("address", {}).get("country", ""),
                 "region": i.get("address", {}).get("state", "Global")} for i in data]
    except: return []