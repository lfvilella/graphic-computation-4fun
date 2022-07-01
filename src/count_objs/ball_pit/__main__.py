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
        # cv2.putText(image, f"#{i + 1}", (int(x) - 45, int(y) + 20),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 5)
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)


def count_ball_from_image(filepath, debug):
    image = cv2.imread(filepath)
    image_original = image.copy()

    # image_blur = cv2.medianBlur(image, 35)

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # lower_yellow0 = np.array([22, 93, 0], dtype="uint8")
    # upper_yellow0 = np.array([45, 255, 255], dtype="uint8")
    # mask0 = cv2.inRange(image_hsv, lower_yellow0, upper_yellow0)
    # lower_yellow1 = np.array([22, 60, 200], np.uint8)
    # upper_yellow1 = np.array([60, 255, 255], np.uint8)
    # mask1 = cv2.inRange(image_hsv, lower_yellow1, upper_yellow1)
    # mask = mask0 + mask1

    # # lower mask (0-10)
    # lower_red0 = np.array([0, 50, 50])
    # upper_red0 = np.array([10, 255, 255])
    # mask0 = cv2.inRange(image_hsv, lower_red0, upper_red0)
    # # upper mask (170-180)
    # lower_red1 = np.array([170, 50, 50])
    # upper_red1 = np.array([180, 255, 255])
    # mask1 = cv2.inRange(image_hsv, lower_red1, upper_red1)
    # mask = mask0 + mask1

    lower_blue0 = np.array([100,150,0], dtype="uint8")
    upper_blue0 = np.array([140,255,255], dtype="uint8")
    mask0 = cv2.inRange(image_hsv, lower_blue0, upper_blue0)
    lower_blue1 = np.array([10, 33, 120], dtype="uint8")  # TODO: PAREI AQUI
    upper_blue1 = np.array([20, 65, 255], dtype="uint8")
    mask1 = cv2.inRange(image_hsv, lower_blue1, upper_blue1)
    mask = mask0  # + mask1
    # mask = mask1

    kernel = np.ones((5, 5), np.uint8)
    image_erosion = cv2.erode(mask, kernel, iterations=2)
    opening = cv2.morphologyEx(image_erosion, cv2.MORPH_OPEN, kernel)
    # gradient = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)

    contours = cv2.findContours(
            opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours = contours[0] if len(contours) == 2 else contours[1]
    # for c in contours:
    #     x, y, w, h = cv2.boundingRect(c)
    #     cv2.rectangle(image_original, (x, y), (x + w, y + h), (36, 255, 12), 2)
    contours = imutils.grab_contours(contours)
    _flag_coins(image_original, contours)

    # cv2.imshow('mask', mask)
    # cv2.imshow('blur', image_blur)
    cv2.imshow('opening', opening)
    cv2.imshow('image_erosion', image_erosion)
    cv2.imshow('original', image_original)
    # cv2.imshow('gradient', gradient)
    cv2.waitKey(0)

    # image_blur = cv2.medianBlur(image, 25)
    # image_blur_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
    # _, image_thresh = cv2.threshold(
    #     image_blur_gray, 240, 255, cv2.THRESH_BINARY_INV)
    #
    # kernel = np.ones((3, 3), np.uint8)
    # opening = cv2.morphologyEx(image_thresh, cv2.MORPH_OPEN, kernel)
    #
    # dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    # _, result_image = cv2.threshold(
    #     dist_transform, 0.3 * dist_transform.max(), 255, 0)
    # result_image = np.uint8(result_image)
    #
    # contours = cv2.findContours(result_image.copy(), cv2.RETR_EXTERNAL,
    #                             cv2.CHAIN_APPROX_SIMPLE)
    # contours = imutils.grab_contours(contours)
    balls_number = len(contours)
    #
    # if debug:
    #     _flag_coins(image, contours)
    #     images_data_to_display = {
    #             'Original Image': image_original,
    #             'Blur Image': image_blur,
    #             'HSV Image': image_hsv,
    #             'Yellow mask': mask,
    #             'Yellow mask 1': mask1,
    #             }
    #     display(images_data_to_display, balls_number)

    return balls_number


@click.command()
@click.option('--filepath', type=str, required=True)
@click.option('--debug', is_flag=True, help="Show images results.")
def main(filepath, debug):
    filepath = Path(filepath)
    if not filepath.is_file():
        raise ValueError(f"Invalid file: '{filepath}'")

    coins_number = count_ball_from_image(filepath.__str__(), debug)
    print(f'Total balls count = {coins_number}')


if __name__ == '__main__':
    main()
