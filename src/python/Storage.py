import os
import glob
import pandas as pd


class Storage:
    """class yang berinteraksi dengan penyimpanan."""
    def __init__(self) -> None:
        self.image_path = None
        self.dataframe_path = None
        self.image_datasets = None

        # Relative path dari folder root
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.parent_directory = os.path.dirname(os.path.dirname(current_directory))

    def save_image_dataset(self) -> None:
        ...

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