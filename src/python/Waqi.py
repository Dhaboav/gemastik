import requests


class Waqi:
    """class untuk berinteraksi dengan layanan waqi.
    
    Attributes:
        base_url (str): link website waqi.
    """
    def __init__(self) -> None:
        self.__base_url = 'https://api.waqi.info/feed/{}/?token={}'

    def request_air_quality_info(self, city: str, api_key: str) -> dict[str]:
        """Melakukan request ke waqi.

        Args:
            city (str): nama kode dari kota.
            api_key (str): kode api dari waqi.
        """
        request_url = self.__base_url.format(city, api_key)
        try:
            response = requests.get(request_url)
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'ok':
                iaqi = data['data']['iaqi']
                air_quality_details = {
                    'PM2.5': iaqi.get('pm25', {}).get('v', 'Data not available'),
                    'PM10': iaqi.get('pm10', {}).get('v', 'Data not available'),
                    'O3': iaqi.get('o3', {}).get('v', 'Data not available'),
                    'SO2': iaqi.get('so2', {}).get('v', 'Data not available'),
                    'NO2': iaqi.get('no2', {}).get('v', 'Data not available'),
                    'CO': iaqi.get('co', {}).get('v', 'Data not available')
                }
                return air_quality_details
            else:
                return f'Error fetching data: {data['data']}'
            
        except requests.exceptions.RequestException as e:
            return f'HTTP Request failed: {e}'