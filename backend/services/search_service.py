import requests

def search_cities(query):
    # Public API - No Key Required
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,
        "limit": 5,
        "featuretype": "city"
    }
    headers = {
        "User-Agent": "TravelBud_Hackathon_App"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        data = response.json()
        
        results = []
        for item in data:
            address = item.get("address", {})
            city_name = address.get("city") or address.get("town") or address.get("village") or item.get("display_name").split(',')[0]
            
            results.append({
                "city": city_name,
                "country": address.get("country", ""),
                "region": address.get("state", address.get("county", "Region"))
            })
        return results
    except Exception as e:
        print(f"API Error: {e}")
        return []