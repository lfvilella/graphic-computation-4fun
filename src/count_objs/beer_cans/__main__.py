from pathlib import Path

import click
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt


def display(images_data: dict, coins_number):
    fig, axis = plt.subplots(1, 5)
    fig.canvas.set_window_title(f'Total coins count = {coins_number}')
    for index, (label, image) in enumerate(images_data.items()):
        axis[index].imshow(image)
        axis[index].set_title(label)
    plt.show()


def _flag_coins(image, contours):
    for (i, c) in enumerate(contours):
        ((x, y), _) = cv2.minEnclosingCircle(c)
        cv2.putText(image, f"#{i + 1}", (int(x) - 45, int(y) + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)


def count_coins_from_image(filepath, debug):
    image = cv2.imread(filepath)
    image_blur = cv2.medianBlur(image, 25)
    image_blur_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
    _, image_thresh = cv2.threshold(
            image_blur_gray, 85, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((10, 10), np.uint8)
    opening = cv2.morphologyEx(image_thresh, cv2.MORPH_OPEN, kernel)

    # cv2.imshow('image', image)
    # cv2.imshow('image_blur', image_blur)
    cv2.imshow('image_blur_gray', image_blur_gray)
    cv2.imshow('image_thresh', image_thresh)
    cv2.imshow('opening', opening)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, result_image = cv2.threshold(
        dist_transform, 0.3 * dist_transform.max(), 255, 0)
    result_image = np.uint8(result_image)

    contours = cv2.findContours(result_image.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    coins_number = len(contours)

    # if debug:
    #     _flag_coins(image, contours)
    #     images_data_to_display = {
    #             'Original Image': cv2.imread(filepath),
    #             'Image Blur': image_blur,
    #             'Image COLOR_BGR2GRAY': image_blur_gray,
    #             'Image result': result_image,
    #             'Image count labels': image,
    #             }
    #     display(images_data_to_display, coins_number)

    return coins_number


@click.command()
@click.option('--filepath', type=str, required=True)
@click.option('--debug', is_flag=True, help="Show images results.")
def main(filepath, debug):
    filepath = Path(filepath)
    if not filepath.is_file():
        raise ValueError(f"Invalid file: '{filepath}'")

    coins_number = count_coins_from_image(filepath.__str__(), debug)
    print(f'Total coins count = {coins_number}')


if __name__ == '__main__':
    main()
