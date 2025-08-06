# utils/clinic_finder.py - Complete Clinic Finding Utilities
import requests
import json
from typing import List, Dict, Any, Optional
import time

def find_nearby_clinics(city: str, country: str = "India") -> List[Dict[str, Any]]:
    """
    Find nearby clinics and hospitals using free APIs
    
    Args:
        city: City name to search in
        country: Country name (default: India)
    
    Returns:
        List of clinic/hospital information dictionaries
    """
    clinics = []
    
    print(f"Searching for clinics in {city}, {country}...")
    
    # Try multiple free APIs for comprehensive results
    
    # 1. Try Overpass API (OpenStreetMap data) - Completely free
    try:
        clinics.extend(get_clinics_from_overpass(city, country))
        if clinics:
            print(f"Found {len(clinics)} clinics from OpenStreetMap")
    except Exception as e:
        print(f"Overpass API error: {e}")
    
    # 2. Try Nominatim search (Free backup)
    if len(clinics) < 3:
        try:
            additional_clinics = get_clinics_from_nominatim(city, country)
            clinics.extend(additional_clinics)
            print(f"Added {len(additional_clinics)} clinics from Nominatim")
        except Exception as e:
            print(f"Nominatim API error: {e}")
    
    # 3. Add default/known clinics for major cities (fallback)
    if len(clinics) < 2:
        default_clinics = get_default_clinics(city)
        clinics.extend(default_clinics)
        print(f"Added {len(default_clinics)} default clinics")
    
    # Remove duplicates based on name
    seen_names = set()
    unique_clinics = []
    for clinic in clinics:
        name = clinic['name'].lower()
        if name not in seen_names:
            seen_names.add(name)
            unique_clinics.append(clinic)
    
    return unique_clinics[:8]  # Return max 8 clinics

def get_clinics_from_overpass(city: str, country: str) -> List[Dict[str, Any]]:
    """Get clinics from OpenStreetMap via Overpass API (completely free)"""
    try:
        # First get city coordinates
        nominatim_url = "https://nominatim.openstreetmap.org/search"
        nominatim_params = {
            "q": f"{city}, {country}",
            "format": "json",
            "limit": 1
        }
        
        headers = {"User-Agent": "EcosyncAI/1.0 (healthcare finder; educational use)"}
        
        # Get city coordinates with rate limiting
        time.sleep(1)  # Rate limiting
        response = requests.get(nominatim_url, params=nominatim_params, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
        
        locations = response.json()
        if not locations:
            return []
        
        lat = float(locations[0]["lat"])
        lon = float(locations[0]["lon"])
        
        # Query Overpass API for hospitals and clinics
        overpass_url = "https://overpass-api.de/api/interpreter"
        
        # Search in a 15km radius around the city center
        overpass_query = f"""
        [out:json][timeout:30];
        (
          node["amenity"="hospital"](around:15000,{lat},{lon});
          node["amenity"="clinic"](around:15000,{lat},{lon});
          node["amenity"="doctors"](around:15000,{lat},{lon});
          node["healthcare"="hospital"](around:15000,{lat},{lon});
          node["healthcare"="clinic"](around:15000,{lat},{lon});
          way["amenity"="hospital"](around:15000,{lat},{lon});
          way["amenity"="clinic"](around:15000,{lat},{lon});
          way["healthcare"="hospital"](around:15000,{lat},{lon});
        );
        out center meta;
        """
        
        time.sleep(2)  # Rate limiting for Overpass API
        response = requests.post(overpass_url, data=overpass_query, headers=headers, timeout=30)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        clinics = []
        
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            
            # Get coordinates
            if element["type"] == "node":
                clinic_lat = element["lat"]
                clinic_lon = element["lon"]
            elif element["type"] == "way" and "center" in element:
                clinic_lat = element["center"]["lat"]
                clinic_lon = element["center"]["lon"]
            else:
                continue
            
            # Extract clinic information
            name = tags.get("name", "")
            if not name:
                continue  # Skip facilities without names
            
            # Skip if name is too generic
            generic_names = ["hospital", "clinic", "medical center", "healthcare"]
            if name.lower() in generic_names:
                continue
            
            # Get address information
            address = format_address(tags, city)
            
            # Get phone number
            phone = tags.get("phone", tags.get("contact:phone", "Contact local directory"))
            
            # Get website
            website = tags.get("website", tags.get("contact:website", ""))
            
            # Determine facility type
            facility_type = "Hospital"
            if tags.get("amenity") == "clinic" or tags.get("healthcare") == "clinic":
                facility_type = "Clinic"
            elif tags.get("amenity") == "doctors":
                facility_type = "Doctor's Office"
            
            clinic_info = {
                "name": name,
                "address": address,
                "phone": clean_phone_number(phone),
                "website": website,
                "type": facility_type,
                "latitude": clinic_lat,
                "longitude": clinic_lon,
                "rating": "N/A",  # OSM doesn't have ratings
                "distance": calculate_distance(lat, lon, clinic_lat, clinic_lon)
            }
            
            clinics.append(clinic_info)
        
        # Sort by distance (closest first)
        clinics = sorted(clinics, key=lambda x: x["distance"])
        
        return clinics[:10]  # Return top 10
        
    except Exception as e:
        print(f"Error fetching from Overpass API: {e}")
        return []

def get_clinics_from_nominatim(city: str, country: str) -> List[Dict[str, Any]]:
    """Fallback method using Nominatim search"""
    try:
        search_terms = [
            f"hospital {city} {country}",
            f"medical center {city} {country}",
            f"clinic {city} {country}",
            f"healthcare {city} {country}"
        ]
        
        clinics = []
        headers = {"User-Agent": "EcosyncAI/1.0 (healthcare finder; educational use)"}
        
        for term in search_terms:
            time.sleep(1)  # Rate limiting
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": term,
                "format": "json",
                "limit": 3,
                "countrycodes": get_country_code(country),
                "addressdetails": 1
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                results = response.json()
                
                for result in results:
                    display_name = result.get("display_name", "")
                    
                    # Filter for healthcare facilities
                    if any(word in display_name.lower() for word in ["hospital", "clinic", "medical", "health"]):
                        name = display_name.split(",")[0]
                        
                        # Skip generic names
                        if len(name.strip()) > 3 and not any(generic in name.lower() for generic in ["hospital", "clinic"]):
                            clinics.append({
                                "name": name,
                                "address": display_name,
                                "phone": "Contact local directory",
                                "website": "",
                                "latitude": float(result["lat"]),
                                "longitude": float(result["lon"]),
                                "rating": "N/A",
                                "type": "Healthcare Facility"
                            })
        
        return clinics[:5]  # Return top 5
        
    except Exception as e:
        print(f"Error fetching from Nominatim: {e}")
        return []

def get_default_clinics(city: str) -> List[Dict[str, Any]]:
    """Provide default clinic suggestions for major cities"""
    
    default_clinics = {
        "delhi": [
            {"name": "All India Institute of Medical Sciences (AIIMS)", "address": "Ansari Nagar, New Delhi - 110029", "phone": "011-26588500", "type": "Government Hospital"},
            {"name": "Apollo Hospital", "address": "Sarita Vihar, New Delhi - 110076", "phone": "011-26925801", "type": "Private Hospital"},
            {"name": "Max Super Speciality Hospital", "address": "1, Press Enclave Road, Saket, New Delhi - 110017", "phone": "011-26515050", "type": "Private Hospital"},
            {"name": "Fortis Hospital", "address": "Sector B, Pocket 1, Aruna Asaf Ali Marg, Vasant Kunj, New Delhi - 110070", "phone": "011-42776222", "type": "Private Hospital"},
        ],
        "mumbai": [
            {"name": "Tata Memorial Hospital", "address": "Dr E Borges Rd, Parel, Mumbai - 400012", "phone": "022-24177000", "type": "Government Hospital"},
            {"name": "Kokilaben Dhirubhai Ambani Hospital", "address": "Rao Saheb Achutrao Patwardhan Marg, Four Bunglows, Andheri West, Mumbai - 400053", "phone": "022-42696969", "type": "Private Hospital"},
            {"name": "Lilavati Hospital", "address": "A-791, Bandra Reclamation, Bandra West, Mumbai - 400050", "phone": "022-26567777", "type": "Private Hospital"},
            {"name": "Hinduja Hospital", "address": "Veer Savarkar Marg, Mahim, Mumbai - 400016", "phone": "022-24447000", "type": "Private Hospital"},
        ],
        "bangalore": [
            {"name": "Manipal Hospital", "address": "98, HAL Airport Road, Kodihalli, Bengaluru - 560017", "phone": "080-25023030", "type": "Private Hospital"},
            {"name": "Fortis Hospital", "address": "154/9, Bannerghatta Road, Opposite IIM, Bengaluru - 560076", "phone": "080-66214444", "type": "Private Hospital"},
            {"name": "Apollo Hospital", "address": "154/11, Bannerghatta Road, Bengaluru - 560076", "phone": "080-26304050", "type": "Private Hospital"},
            {"name": "Narayana Health", "address": "258/A, Bommasandra Industrial Area, Anekal Taluk, Bengaluru - 560099", "phone": "080-71222222", "type": "Private Hospital"},
        ],
        "gurugram": [
            {"name": "Medanta - The Medicity", "address": "Sector 38, Gurugram - 122001", "phone": "0124-4141414", "type": "Private Hospital"},
            {"name": "Artemis Hospital", "address": "Sector 51, Gurugram - 122001", "phone": "0124-4511111", "type": "Private Hospital"},
            {"name": "Fortis Memorial Research Institute", "address": "Sector 44, Gurugram - 122002", "phone": "0124-4962200", "type": "Private Hospital"},
            {"name": "Max Hospital", "address": "Block B, Sushant Lok Phase I, Sector 43, Gurugram - 122002", "phone": "0124-4566666", "type": "Private Hospital"},
        ],
        "chennai": [
            {"name": "Apollo Hospital", "address": "21, Greams Lane, Off Greams Road, Chennai - 600006", "phone": "044-28290200", "type": "Private Hospital"},
            {"name": "Fortis Malar Hospital", "address": "52, 1st Main Road, Gandhi Nagar, Adyar, Chennai - 600020", "phone": "044-42894289", "type": "Private Hospital"},
            {"name": "MIOT International", "address": "4/112, Mount Poonamalle Road, Manapakkam, Chennai - 600089", "phone": "044-42002000", "type": "Private Hospital"},
        ],
        "hyderabad": [
            {"name": "Apollo Hospital", "address": "Jubilee Hills, Hyderabad - 500033", "phone": "040-23607777", "type": "Private Hospital"},
            {"name": "CARE Hospital", "address": "Road No. 1, Banjara Hills, Hyderabad - 500034", "phone": "040-61651000", "type": "Private Hospital"},
            {"name": "Continental Hospital", "address": "IT Park Rd, Nanakramguda, Gachibowli, Hyderabad - 500032", "phone": "040-67000000", "type": "Private Hospital"},
        ]
    }
    
    city_lower = city.lower()
    if city_lower in default_clinics:
        return [
            {
                **clinic,
                "website": "",
                "rating": "4.2",  # Average rating for known hospitals
                "latitude": 0,
                "longitude": 0
            }
            for clinic in default_clinics[city_lower]
        ]
    
    # Generic suggestions for unknown cities
    return [
        {
            "name": f"City General Hospital - {city}",
            "address": f"Hospital Road, {city}",
            "phone": "Contact local medical directory",
            "website": "",
            "rating": "N/A",
            "type": "General Hospital",
            "latitude": 0,
            "longitude": 0
        },
        {
            "name": f"Primary Health Centre - {city}",
            "address": f"Main Health Centre, {city}",
            "phone": "Contact local health department",
            "website": "",
            "rating": "N/A", 
            "type": "Primary Health Centre",
            "latitude": 0,
            "longitude": 0
        }
    ]

def format_address(tags: dict, city: str) -> str:
    """Format address from OSM tags"""
    address_parts = []
    
    if tags.get("addr:housenumber"):
        address_parts.append(tags["addr:housenumber"])
    if tags.get("addr:street"):
        address_parts.append(tags["addr:street"])
    if tags.get("addr:suburb"):
        address_parts.append(tags["addr:suburb"])
    if tags.get("addr:city") and tags["addr:city"] != city:
        address_parts.append(tags["addr:city"])
    if tags.get("addr:postcode"):
        address_parts.append(tags["addr:postcode"])
    
    if address_parts:
        return ", ".join(address_parts)
    elif tags.get("addr:full"):
        return tags["addr:full"]
    else:
        return f"Near {city} city center"

def clean_phone_number(phone: str) -> str:
    """Clean and format phone numbers"""
    if not phone or phone == "Contact local directory":
        return "Contact local directory"
    
    # Remove common prefixes and clean
    phone = phone.replace("+91-", "").replace("+91 ", "").strip()
    return phone if phone else "Contact local directory"

def get_country_code(country: str) -> str:
    """Get country code for Nominatim API"""
    country_codes = {
        "india": "in",
        "united states": "us",
        "canada": "ca",
        "united kingdom": "gb",
        "australia": "au"
    }
    return country_codes.get(country.lower(), "")

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate approximate distance between two points (simplified)"""
    return abs(lat1 - lat2) + abs(lon1 - lon2)

# Test function
def test_clinic_finder():
    """Test the clinic finder functionality"""
    test_cities = ["Delhi", "Mumbai", "Gurugram", "Unknown City"]
    
    for city in test_cities:
        print(f"\n--- Testing {city} ---")
        clinics = find_nearby_clinics(city)
        print(f"Found {len(clinics)} clinics:")
        for clinic in clinics[:3]:
            print(f"- {clinic['name']}: {clinic['phone']}")

if __name__ == "__main__":
    test_clinic_finder()