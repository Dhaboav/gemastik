import requests
import threading


class RequestPost:
    """class untuk mengirim data ke web GIS.
    
    Attributes:
        url (str): URL link API web.
    """
    def __init__(self, url) -> None:
        self.url = url

    def post(self, data: dict, image_path: str) -> None:
        """Merequest post ke web GIS.

        Args:
            data (dict): Data sensor.
            image_path (str): Path dari gambar.
        """
        def post_request():
            try:
                with open(image_path, 'rb') as file:
                    files = {'n_gambar': (image_path, file, 'image/png')}
                    response = requests.post(self.url, data=data, files=files)
                    print(response.text)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

        # Run thread
        threading.Thread(target=post_request).start()