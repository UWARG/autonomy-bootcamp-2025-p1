"""
Detects colours on a map of landing pads.
"""

from pathlib import Path
import cv2
import numpy as np


class DetectBlue:
    """Detects blue objects from an image."""

    __create_key = object()

    @classmethod
    def create(cls) -> "DetectBlue":
        """Factory method to create DetectBlue instance."""
        return DetectBlue(cls.__create_key)

    def __init__(self, class_create_private_key: object) -> None:
        """Private constructor, use create() method."""
        if class_create_private_key is not DetectBlue.__create_key:
            raise ValueError("Use create() method")

    def run(self, image: str, output_path: Path, return_mask: bool = False) -> None | np.ndarray:
        """
        Detects blue from an image, annotates contours, and optionally returns the mask.

        Args:
            image: Path to the input image.
            output_path: Path to save the annotated output image.
            return_mask: If True, returns the mask of detected blue areas.

        Returns:
            The mask if return_mask is True, else None.
        """
        img = cv2.imread(image)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Blue colour range in HSV
        lower_blue = np.array([100, 150, 50])
        upper_blue = np.array([140, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        _ = cv2.bitwise_and(img, img, mask=mask)  # Prevent unused variable warning

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
        cv2.imwrite(str(output_path), img)

        if return_mask:
            return mask
        return None


class DetectRed:
    """Detects red objects from an image."""

    __create_key = object()

    @classmethod
    def create(cls) -> "DetectRed":
        """Factory method to create DetectRed instance."""
        return DetectRed(cls.__create_key)

    def __init__(self, class_create_private_key: object) -> None:
        """Private constructor, use create() method."""
        if class_create_private_key is not DetectRed.__create_key:
            raise ValueError("Use create() method")

    def run(self, image: str, output_path: Path, return_mask: bool = False) -> None | np.ndarray:
        """
        Detects red from an image, annotates contours, and optionally returns the mask.

        Args:
            image: Path to the input image.
            output_path: Path to save the annotated output image.
            return_mask: If True, returns the mask of detected red areas.

        Returns:
            The mask if return_mask is True, else None.
        """
        img = cv2.imread(image)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Red colour range in HSV (wrap-around)
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 | mask2
        _ = cv2.bitwise_and(img, img, mask=mask)  # Prevent unused variable warning

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
        cv2.imwrite(str(output_path), img)

        if return_mask:
            return mask
        return None
