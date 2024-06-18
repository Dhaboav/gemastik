import os
import cv2
import glob
import pandas as pd


class Storage:
    """class yang berinteraksi dengan penyimpanan.
    
    Attributes:
        datasets_path (str): Path referensi ke datasets.
        capture_count (int): Penghitung buat gambar.
        parent_directory (str): Path relative file terhadap root.
    """
    def __init__(self) -> None:
        self.datasets_path = None
        self.capture_count = 0

        # Relative path dari folder root
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.parent_directory = os.path.dirname(os.path.dirname(current_directory))

    def save_image_dataset(self, image) -> None:
        """Menyimpan gambar.

        Args:
            image (cv2): Gambar dari opencv.
        """
        dataset_path = os.path.join(self.parent_directory, self.datasets_path)
        image_format_name = f'img-{self.capture_count}.jpg'
        image_path = os.path.join(dataset_path, image_format_name)
        cv2.imwrite(image_path, image)
        self.capture_count += 1
        
    def save_pandas_dataframe(self, data: dict, filename='basisData.csv') -> None:
        """Menyimpan data sensor ke csv format.

        Args:
            data (dict/json): Data dari sensor.
            filename (str): nama file (default: basisData.csv)
        """
        df = pd.DataFrame([data])
        path = os.path.join(self.parent_directory, self.datasets_path)
        full_path = os.path.join(path, filename)
        
        if not os.path.isfile(full_path):
            df.to_csv(full_path, mode='w', header=True, index=False)
        else:
            df.to_csv(full_path, mode='a', header=False, index=False)

    def load_image_dataset(self) -> list:
        """Pengaksesan file gambar dengan format png, jpeg, dan jpg.

        Returns:
            list: Path dari file gambar yang cocok dengan pattern.
        """
        dataset_path = os.path.join(self.parent_directory, self.datasets_path)
        image_patterns = ['*.png', '*.jpeg', '*.jpg']
        images = []
        for pattern in image_patterns:
            images.extend(glob.glob(os.path.join(dataset_path, pattern)))
        return images

    def set_datasets_path(self, path: str) -> None:
        """Set path untuk dataframe pandas.

        Args:
            path (str): nama folder pandas.
        """
        self.datasets_path = path