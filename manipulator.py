from numpy.typing import NDArray
from numpy import uint8
import cv2
import argparse

def load_image_file(file: str) -> tuple[NDArray[uint8], str, str]:
    """
    Load the contents of an image file and return as a list of strings.

    Args:
        file (str): The location of the file to be loaded.

    Returns:
        NDArray[uint8]: The image as a NumPy array with shape (height, width, channels) 
            where channels is 3 for a color image (BGR) and 1 for grayscale.
        str: The name of the file without path or extension.
        str: The extension of the file (e.g. .png).
    
    Raises:
        ValueError: If the file has an invalid file type.
    """
    # confirm filetype
    valid_file_types = ['bmp', 'jpg', 'png']
    file_type = file.split('.')[-1]
    if file_type not in valid_file_types:
        raise ValueError(f'Invalid file type: {file_type}')
    # get image name without path or extension
    image_name = file.split('/')[-1].split('.')[0]
    image =  cv2.imread(file)
    return image, image_name, file_type

def make_grayscale(image: NDArray[uint8]) -> NDArray[uint8]:
    """
    Convert an image to grayscale.

    Args:
        image (NDArray[uint8]): The image to be converted.

    Returns:
        NDArray[uint8]: The converted image in grayscale.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def make_thumbnail(image: NDArray[uint8], width: int = None, height: int = None) -> NDArray[uint8]:
    """
    Create a thumbnail of an image. Height and width are optional. 
    If height & width are not provided it will scale the image to a height of 128 pixels.

    Args:
        image (NDArray[uint8]): The image to be converted to a thumbnail..
        width (int): (Optional) The width of the thumbnail.
        height (int): (Optional) The height of the thumbnail.

    Returns:
        NDArray[uint8]: The thumbnail image.
    """
    if width is None and height is None:
        height = 128
        original_height, original_width = image.shape[:2]
        scale_factor = height / original_height
        width = int(original_width * scale_factor)
    return cv2.resize(image, (width, height))

def save_image(file: str, image: NDArray[uint8]) -> None:
    """
    Save an image to disk.
    """
    try:
        cv2.imwrite(file, image)
    except Exception as e:
        print(f"Error writing file to disk: {e}")


def main():
    parser = argparse.ArgumentParser(description="Image Manipulator")
    parser.add_argument('--input', type=str, help='Input file path', default='./lena.png')
    parser.add_argument('--output', type=str, help='Output file directory', default='./')
    args = parser.parse_args()

    # Access the arguments
    input_path = args.input
    output_path = args.output

    # Rest of your program here
    print(f"Loading image: {input_path} and saving to: {output_path}")
    # get image name without extension or path
    image, image_name, image_type = load_image_file(input_path)
    image_grayscale = make_grayscale(image)
    image_thumbnail = make_thumbnail(image_grayscale)
    cv2.imwrite(f"{output_path}{image_name}_grayscale.{image_type}", image_grayscale)
    cv2.imwrite(f"{output_path}{image_name}_thumbnail.{image_type}", image_thumbnail)

if __name__ == "__main__":
    main()