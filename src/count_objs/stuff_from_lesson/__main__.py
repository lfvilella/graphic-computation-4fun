from pathlib import Path

import click
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt


def display(images_data: dict, coins_number):
    for index, (label, image) in enumerate(images_data.items()):
        plt.subplot(3, 3, index + 1)
        plt.imshow(image, 'gray', vmin=0, vmax=255)
        plt.title(label)
        plt.xticks([])
        plt.yticks([])
    plt.show()
    # fig, axis = plt.subplots(1, len(images_data))
    # fig.canvas.set_window_title(f'Total coins count = {coins_number}')
    # for index, (label, image) in enumerate(images_data.items()):
    #     axis[index].imshow(image)
    #     axis[index].set_title(label)
    # plt.show()


def _flag_coins(image, contours):
    for (i, c) in enumerate(contours):
        ((x, y), _) = cv2.minEnclosingCircle(c)
        cv2.putText(image, f"#{i + 1}", (int(x) - 45, int(y) + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)


def shadow_remove(img):
    rgb_planes = cv2.split(img)
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_norm_planes.append(norm_img)
    shadow_removed = cv2.merge(result_norm_planes)
    return shadow_removed


def __count_stuff_from_image(filepath, debug):
    image = cv2.imread(filepath)
    image_blur_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image_blur = cv2.medianBlur(image, 25)
    # image_blur_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
    # _, image_thresh = cv2.threshold(
    #     image_blur_gray, 127, 255, cv2.THRESH_BINARY_INV)
    #
    # kernel = np.ones((3, 3), np.uint8)
    # opening = cv2.morphologyEx(image_thresh, cv2.MORPH_OPEN, kernel)

    shadow_removed = shadow_remove(image_blur_gray)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(shadow_removed, cv2.MORPH_OPEN, kernel)
    _, image_thresh = cv2.threshold(opening, 127, 255, cv2.THRESH_BINARY_INV)

    # contours = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL,
    #                             cv2.CHAIN_APPROX_SIMPLE)
    # contours = imutils.grab_contours(contours)
    # coins_number = len(contours)
    # print(f"{coins_number=}")
    # _flag_coins(image, contours)

    cv2.imshow('img', image_thresh)
    cv2.waitKey(0)


def adjust_gamma(image, gamma=1.0):
   invGamma = 1.0 / gamma
   table = np.array([
      ((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)])
   return cv2.LUT(image.astype(np.uint8), table.astype(np.uint8))


def _latest_count_stuff_from_image(filepath, debug):
    image = cv2.imread(filepath)
    image_gama = adjust_gamma(image, 0.1)
    shadow_removed = shadow_remove(image_gama)
    image_blur_gray = cv2.cvtColor(shadow_removed, cv2.COLOR_BGR2GRAY)
    image_blur = cv2.medianBlur(image_blur_gray, 25)
    #
    # image = cv2.imread(filepath)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # do adaptive threshold on gray image
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    #                                cv2.THRESH_BINARY, 51, 25)



    result = image_blur
    contours = cv2.findContours(result.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    coins_number = len(contours)
    print(f"{coins_number=}")
    _flag_coins(image, contours)

    images_data_to_display = {
        'Original Image': cv2.imread(filepath),
        # 'Gray Image': gray,
        'Image Blur': image_blur,
        'Image gama': image_gama,
        'Image COLOR_BGR2GRAY': image_blur_gray,
        'Image shadow removed': shadow_removed,
        # 'Image thresh': thresh,
        # 'Image opening': opening,
        'Image count labels': image,
    }
    display(images_data_to_display, coins_number)


def count_stuff_from_image(filepath, debug):
    image = cv2.imread(filepath)
    image_blur = cv2.medianBlur(image, 25)
    image_blur_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)

    shadow_removed = shadow_remove(image_blur_gray)
    _, image_thresh = cv2.threshold(
        shadow_removed, 200, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(image_thresh, cv2.MORPH_OPEN, kernel)

    contours = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    coins_number = len(contours)
    print(f"{coins_number=}")
    _flag_coins(image, contours)

    images_data_to_display = {
            'Original Image': cv2.imread(filepath),
            'Image Blur': image_blur,
            'Image Gray': image_blur_gray,
            'Image Shadow Removed': shadow_removed,
            'Image Thresh': image_thresh,
            'Image Opening': opening,
            'Image Count Labels': image,
            }
    display(images_data_to_display, coins_number)


@click.command()
@click.option('--filepath', type=str, required=True)
@click.option('--debug', is_flag=True, help="Show images results.")
def main(filepath, debug):
    filepath = Path(filepath)
    if not filepath.is_file():
        raise ValueError(f"Invalid file: '{filepath}'")

    coins_number = count_stuff_from_image(filepath.__str__(), debug)
    print(f'Total stuff count = {coins_number}')


if __name__ == '__main__':
    main()
