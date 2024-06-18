import os
import cv2
import glob
import pandas as pd


class Storage:
    """class yang berinteraksi dengan penyimpanan.
    
    Attributes:
        image_path (str): Path untuk menyimpan gambar.
        dataframe_path (str): Path untuk menyimpan dataframe pandas.
        image_datasets (str): Path untuk pengaksesan datasets gambar.
        capture_count (int): Counter Cek.
        parent_directory (str): Path relative file terhadap root.
    """
    def __init__(self) -> None:
        self.image_path = None
        self.dataframe_path = None
        self.image_datasets = None
        self.capture_count = 0

        # Relative path dari folder root
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.parent_directory = os.path.dirname(os.path.dirname(current_directory))

    def save_image_dataset(self, image) -> None:
        """Menyimpan gambar.

        Args:
            image (cv2): Gambar dari opencv.
        """
        dataset_path = os.path.join(self.parent_directory, self.image_path)
        image_format_name = f'img-{self.capture_count}.jpg'
        image_path = os.path.join(dataset_path, image_format_name)
        cv2.imwrite(image_path, image)
        self.capture_count += 1
        
    def save_pandas_dataframe(self) -> None:
        ...

    def load_image_dataset(self) -> list:
        """Pengaksesan file gambar dengan format png, jpeg, dan jpg.

        Returns:
            list: Path dari file gambar yang cocok dengan pattern.
        """
        dataset_path = os.path.join(self.parent_directory, self.image_datasets)
        image_patterns = ['*.png', '*.jpeg', '*.jpg']
        images = []
        for pattern in image_patterns:
            images.extend(glob.glob(os.path.join(dataset_path, pattern)))
        return images

    def set_image_path(self, path: str) -> None:
        """Set path untuk menyimpan gambar yang diambil.

        Args:
            path (str): nama folder datasets.
        """
        self.image_path = path

    def set_dataframe_path(self, path: str) -> None:
        """Set path untuk dataframe pandas.

        Args:
            path (str): nama folder pandas.
        """
        self.dataframe_path = path

    def set_image_datasets(self, path: str) -> None:
        """Set path dari datasets untuk gambar.

        Args:
            path (str): nama folder datasets.
        """
        self.image_datasets = path