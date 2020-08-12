import os

from PIL import Image, UnidentifiedImageError


def files(path: str) -> list:
    "Return list of all files in directory"
    if path == '':
        path = '.'
    for (_, _, filenames) in os.walk(path):
        return filenames
    raise ValueError(f"Incorrect path: {path}")


def scale(image: Image, size: str) -> tuple:
    "Return scaled size (width, height) of image"
    if size[-1] == '%':
        factor = float(size[:-1])/100
    else:
        factor = min(  # choose longer side
            float(size)/image.width,
            float(size)/image.height)
    width = round(image.width * factor)
    height = round(image.height * factor)
    return width, height


def resize():
    """
    Change size and copy all images from one directory to another.

    Image sides can be scaled with percentage value
    or with an align of a longer side to a given pixel value.

    Sides ratio may slightly change due to float -> intiger rounding.
    """
    copy_from = input("Copy from: ").strip()
    copy_to = input("Copy to: ").strip()
    size = input("""Enter size in form of:
    -integer, example: 500 (size of longer side in pixels)
    -percent, example: 50% (percent which whole image will be scaled by)\n""").strip()
    failures = []
    images = files(copy_from)
    length = len(images)

    print("Start resizing...")

    for index, name in enumerate(images, 1):
        print(f"Copying {index} out of {length} images...", end='\r')
        path_to_image = os.path.join(copy_from, name)
        try:
            image = Image.open(path_to_image)
        except UnidentifiedImageError:
            failures.append(name)
            continue
        new_size = scale(image, size)
        resized_image = image.resize(new_size, Image.ANTIALIAS)
        filename, extension = name.rsplit('.', 1)
        save_path = os.path.join(copy_to, f"{filename}-resized.{extension}")
        resized_image.save(save_path)

    if not failures:
        print("\nAll images resized successfully")
    else:
        print("\nResizing has failed for:", *failures, sep='\n')
    input("\nPress Enter to quit...")


if __name__ == "__main__":
    resize()
