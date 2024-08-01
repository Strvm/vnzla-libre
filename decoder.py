import json
import os
from PIL import Image
from cv2 import imread
from pyzbar.pyzbar import decode, ZBarSymbol
from qreader import QReader
from tqdm import tqdm


class Decoder:
    """
    A class to decode QR codes from images and manage the resulting data.

    Attributes:
        base_path (str): The path to the directory containing images.
        all_data (list): A list to store all decoded data.
        existing_data (dict): A dictionary to store data loaded from an existing file.
        cant_parse (list): A list of images that cannot be parsed.
    """

    def __init__(self, base_path):
        """
        Initializes the Decoder with a base path for image files.

        Args:
            base_path (str): The path to the directory containing images.
        """
        self.base_path = base_path
        self.all_data = []
        self.existing_data = {}
        self.cant_parse = []

    def load_existing_data(self, output_file):
        """
        Loads existing data from a JSON file if it exists.

        Args:
            output_file (str): The path to the JSON file containing existing data.
        """
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                self.existing_data = json.load(f)
                self.all_data = self.existing_data
                print(f"Loaded existing data from {output_file}")

    def load_cant_parse_list(self):
        """
        Loads a list of image paths that cannot be parsed from a text file.
        """
        if os.path.exists("track/cant_decode_qr.txt"):
            with open("track/cant_decode_qr.txt") as f:
                self.cant_parse = [line.strip() for line in f.readlines()]

    def decode_images(self):
        """
        Decodes QR codes from all images in the base path directory.
        """
        image_files = [f for f in os.listdir(self.base_path) if f.endswith(".jpg")]

        for image_path in tqdm(image_files):
            if self.is_image_already_processed(image_path):
                continue

            image = Image.open(os.path.join(self.base_path, image_path))
            decoded_data = self.decode_qr_code(image_path, image)

            if decoded_data:
                acta_id = decoded_data.split("!")[0]
                self.all_data.append(
                    {"image_path": image_path, "data": decoded_data, "acta_id": acta_id}
                )

    def is_image_already_processed(self, image_path):
        """
        Checks if an image has already been processed.

        Args:
            image_path (str): The path of the image file.

        Returns:
            bool: True if the image is already processed or cannot be parsed, False otherwise.
        """
        return (
            any(data["image_path"] == image_path for data in self.all_data)
            or image_path in self.cant_parse
        )

    def decode_qr_code(self, image_path, image):
        """
        Decodes a QR code from an image using pyzbar and a backup method if necessary.

        Args:
            image_path (str): The path of the image file.
            image (PIL.Image): The image object to decode.

        Returns:
            str or None: The decoded data from the QR code, or None if decoding failed.
        """
        decoded_objects = decode(image, symbols=[ZBarSymbol.QRCODE])

        if not decoded_objects:
            decoded_data = self.other_decode_method(
                os.path.join(self.base_path, image_path)
            )
            if not decoded_data:
                self.log_cant_parse(image_path)
                return None
        else:
            decoded_data = decoded_objects[0].data.decode("utf-8")

        return decoded_data

    def other_decode_method(self, img_path):
        """
        Uses an alternative method to decode a QR code from an image file.

        Args:
            img_path (str): The path of the image file.

        Returns:
            str or None: The decoded data from the QR code, or None if decoding failed.
        """
        qreader_reader = QReader()
        img = imread(img_path)
        cropped_img = self.crop_image_bottom(img, 0.89)
        cropped_img_path = "cropped_image.png"
        Image.fromarray(cropped_img).save(cropped_img_path)

        qreader_out = qreader_reader.detect_and_decode(image=cropped_img)
        return qreader_out[0] if qreader_out else None

    @staticmethod
    def crop_image_bottom(img, crop_ratio):
        """
        Crops the bottom portion of an image based on a given ratio.

        Args:
            img (numpy.ndarray): The image array to crop.
            crop_ratio (float): The ratio of the image height to retain.

        Returns:
            numpy.ndarray: The cropped image array.
        """
        height, width = img.shape[:2]
        crop_height = int(height * crop_ratio)
        return img[crop_height:, :]

    def log_cant_parse(self, image_path):
        """
        Logs an image path to a file when its QR code cannot be parsed.

        Args:
            image_path (str): The path of the image file.
        """
        with open("track/cant_decode_qr.txt", "a") as f:
            f.write(image_path + "\n")

    def save_data_to_json(self, output_file):
        """
        Saves all decoded data to a JSON file.

        Args:
            output_file (str): The path to the JSON file where data will be saved.
        """
        with open(output_file, "w") as f:
            json.dump(self.all_data, f, indent=4)


if __name__ == "__main__":
    base_path = "./images/"
    output_file = "outputs/qr_data.json"

    decoder = Decoder(base_path)
    decoder.load_existing_data(output_file)
    decoder.load_cant_parse_list()
    decoder.decode_images()
    decoder.save_data_to_json(output_file)
