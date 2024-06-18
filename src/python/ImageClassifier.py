import numpy as np


class ImageClassifier:
    """class untuk mengklasifikasi gambar."""
    def __calculation_variance(self, image) -> int:
        """Kalkulasi nilai varians berdasarkan dimensi gambar (Private).

        Args:
            image (cv2): Gambar.

        Returns:
            int: Nilai mean varians.
        """
        height, width = image.shape
        if not width or not height: 
            return 0
        
        vars = []
        for y in range(height):
            row = image[y, :]
            mean = np.mean(row)
            variance = np.mean((row - mean) ** 2)
            vars.append(variance)
        mean_variance = np.mean(vars)

        return int(mean_variance)
    
    def image_classification(self, image) -> str:
        """Mengklasifikasikan gambar berdasarkan nilai varians.

        Args:
            image (cv2): Gambar.

        Returns:
            str: Kelas dari gambar (Cerah atau Kabut).
        """
        variance_value = self.__calculation_variance(image=image)
        if variance_value > 200:
            return 'Cerah'
        else:
            return 'Kabut'