import os
import argparse
from PIL import Image, ImageOps, UnidentifiedImageError

class BulkImageProcessor: 
    def __init__(self, paths) -> None:
        '''Takes in list of file path and/or directories. Process any images within them'''
        self.images = []
        for path in paths:
            if os.path.isfile(path):
                try:
                    self.images.append(Image.open(path))
                except UnidentifiedImageError as e:
                    print(f"{path} is not an image file, skipping")
            elif os.path.isdir(path):
                for filename in os.listdir(path):
                    filepath = os.path.join(path, filename)
                    if os.path.isfile(filepath):
                        try:
                            self.images.append(Image.open(filepath))
                        except UnidentifiedImageError as e:
                            print(f"{filepath} is not an image file, skipping")


    def resize(self, size):
        for i, image in enumerate(self.images):
            image = image.resize(size)
            self.images[i] = image


    def save(self, prefix, output_dir=None):
        if not output_dir:
            output_dir = "output"
        i = 0
        while os.path.exists(f"{output_dir}-{i}"):
            i += 1
        output_dir = f"{output_dir}-{i}"
        os.makedirs(output_dir)
        for i, image in enumerate(self.images):
            image_path = os.path.join(output_dir, f'{prefix}-{i}.png')
            if os.path.exists(image_path):
                raise Exception(f'File {image_path} already exists, will not overwrite')
            image.save(image_path)


    def colorize(self, rgb_color):
        colorized_images = []
        for img in self.images:
            grayscale_image = ImageOps.grayscale(img)
            color = rgb_color
            print(rgb_color)
            colorized_image = ImageOps.colorize(grayscale_image, black="black", white="white", mid=color)
            colorized_images.append(colorized_image)
        self.images = colorized_images

    def to_grayscale(self):
        grayscale_images = []
        for img in self.images:
            grayscale_image = ImageOps.grayscale(img)
            grayscale_images.append(grayscale_image)
        self.images = grayscale_images



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk Image Processor")
    parser.add_argument('file_paths', type=str, nargs='+',
                        help='List of file paths to process')
    parser.add_argument('-s', '--size', type=int, nargs=2,
                        help='Size to resize images')
    parser.add_argument('-p', '--prefix', type=str,
                        help='Prefix for the filename when saving images')
    parser.add_argument('-c', '--color', type=int, nargs=3,
                        help='Color for the images to be changed into')
    parser.add_argument('-g', '--grayscale', action='store_true',
                        help='Convert images to grayscale')

    
    args = parser.parse_args()

    bim = BulkImageProcessor(args.file_paths)
    if args.size:
        bim.resize(args.size)
    if args.color:
        bim.colorize(args.color)
    if args.grayscale:
        bim.to_grayscale()
    if args.prefix:
        bim.save(args.prefix)

