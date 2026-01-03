import requests

def get_activities(city_name):
    # Overpass API is a free read-only API for OpenStreetMap
    url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:25];
    area[name="{city_name}"]->.searchArea;
    (
      node["tourism"="attraction"](area.searchArea);
      node["tourism"="museum"](area.searchArea);
    );
    out body 10;
    """
    try:
        response = requests.get(url, params={'data': query}, timeout=5)
        data = response.json()
        return [{"name": e.get('tags', {}).get('name', 'Attraction'), 
                 "type": e.get('tags', {}).get('tourism', 'Point of Interest').capitalize()} 
                for e in data.get('elements', []) if 'name' in e.get('tags', {})]
    except:
        return []