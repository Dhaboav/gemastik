import json
import requests


def get_air_quality_details(city: str, api_key: str):
    base_url = 'https://api.waqi.info/feed/{}/?token={}'
    request_url = base_url.format(city, api_key)
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] == "ok":
            iaqi = data["data"]["iaqi"]
            air_quality_details = {
                "PM2.5": iaqi.get("pm25", {}).get("v", "Data not available"),
                "PM10": iaqi.get("pm10", {}).get("v", "Data not available"),
                "O3": iaqi.get("o3", {}).get("v", "Data not available"),
                "SO2": iaqi.get("so2", {}).get("v", "Data not available"),
                "NO2": iaqi.get("no2", {}).get("v", "Data not available"),
                "CO": iaqi.get("co", {}).get("v", "Data not available")
            }
            return air_quality_details
        else:
            return f"Error fetching data: {data['data']}"
    except requests.exceptions.RequestException as e:
        return f"HTTP Request failed: {e}"

def main():
    with open('setup.json', 'r') as file:
        json_file = json.load(file)

    api_key = json_file['WAQI_API_KEY']
    city = json_file['city_code']
    air_quality_details = get_air_quality_details(city, api_key)
    print(air_quality_details)

if __name__ == '__main__':
    main()