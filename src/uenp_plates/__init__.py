import abc
from datetime import datetime
from typing import Optional
from pathlib import Path

import cv2
import imutils
import matplotlib.pyplot as plt
from munch import Munch
import pytesseract


PATH = Path(__name__).parent
OUTPUT_PATH = PATH / 'outputs/uenp_plates'
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


class BaseImageProcessing(metaclass=abc.ABCMeta):
    def __init__(self, image_path: str):
        self.original_image = self._get_original_image(image_path)
        self.metadata = Munch()

    def _get_original_image(self, image):
        if isinstance(image, str):
            image = cv2.imread(image)
        return image

    @abc.abstractmethod
    def pre_processing(self):
        pass

    @abc.abstractmethod
    def segmentation(self, pre_processing):
        pass

    @abc.abstractmethod
    def interpretation(self, segmentation):
        pass

    def process(self):
        pre_processing = self.pre_processing()
        segmentation = self.segmentation(pre_processing)
        interpretation = self.interpretation(segmentation)
        return interpretation

    def _check_has_metadata(self):
        if not self.metadata:
            raise ValueError('The algorithm was not processed yet, please call'
                             '`instance.process()` before display')

    def _get_images_data_to_display(self) -> Optional[dict]:
        # Not an abstractmethod because inheritances could implement it
        #   to debug or not
        return

    def _get_or_raise_images_data_to_display(
            self,
            images_data_to_display: Optional[dict] = None,
            ):
        images_data_to_display = (images_data_to_display
                                  or self._get_images_data_to_display())
        if images_data_to_display is None:
            raise NotImplemented(
                "The private method '_get_images_data_to_display' "
                "was not implemented yet")

        return images_data_to_display

    def _display_image_processing_steps(
            self,
            rows_number,
            columns_number,
            images_data_to_display: Optional[dict] = None,
            window_title: str = 'Image processing flow'):
        images_data_to_display = self._get_or_raise_images_data_to_display(
                images_data_to_display)

        fig, axis = plt.subplots(rows_number, columns_number)
        fig.canvas.set_window_title(window_title)
        row = 0
        for index, (label, image) in enumerate(images_data_to_display.items()):
            column = index % columns_number
            if index != 0 and column == 0:
                row += 1
            axis[row][column].imshow(image)
            axis[row][column].set_title(label)
        plt.show()

    def display(self, rows_number, columns_number):
        # Not an abstractmethod because inheritances could implement it
        #   to debug or not
        return

    def _export_images(
            self,
            images_data_to_display: Optional[dict] = None,
            output_path: Optional[Path] = None
            ):
        images_data_to_display = self._get_or_raise_images_data_to_display(
            images_data_to_display)
        if output_path is None:
            now = datetime.now()
            output_path = (
                OUTPUT_PATH / f"output_{now.strftime('%Y-%m-%d_%H-%M-%S')}")
        output_path.mkdir(parents=True, exist_ok=True)
        for label, image in images_data_to_display.items():
            cv2.imwrite(f"{output_path / label}.jpg", image)

    def export(self):
        # Not an abstractmethod because inheritances could implement it
        #   to debug or not
        return

    def _flag_contours(self, image, contours, inplace: bool = False):
        image_ = image.copy() if not inplace else image
        for (i, c) in enumerate(contours):
            ((x, y), _) = cv2.minEnclosingCircle(c)
            cv2.putText(image_, f"#{i + 1}", (int(x) - 45, int(y) + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            cv2.drawContours(image_, [c], -1, (0, 255, 0), 2)
        return image_


class FindPlates(BaseImageProcessing):
    def pre_processing(self, blur_value: int = 35):
        image = self.original_image.copy()
        image_blur = cv2.medianBlur(image, blur_value)
        image_blur_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
        self.metadata.pre_processing = Munch(image_blur=image_blur,
                                             image_blur_gray=image_blur_gray)
        return image_blur_gray

    def segmentation(
            self,
            pre_processing,
            lower_thresh_margin: int = 127,
            upper_thresh_margin: int = 255,
            ):
        _, image_thresh = cv2.threshold(pre_processing,
                                        lower_thresh_margin,
                                        upper_thresh_margin,
                                        cv2.THRESH_BINARY_INV)
        self.metadata.segmentation = Munch(image_thresh=image_thresh)
        return image_thresh

    def interpretation(self, segmentation):
        contours = cv2.findContours(segmentation.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        self.metadata.interpretation = Munch(contours=contours,
                                             plates_number=len(contours))
        return contours

    def _get_images_data_to_display(self) -> Optional[dict]:
        self._check_has_metadata()
        image_flagged = self._flag_contours(
                self.original_image, self.metadata.interpretation.contours)
        return {'1-original': self.original_image,
                '2-blur': self.metadata.pre_processing.image_blur,
                '3-gray': self.metadata.pre_processing.image_blur_gray,
                '4-thresh': self.metadata.segmentation.image_thresh,
                '5-labels': image_flagged}

    def display(self):
        self._display_image_processing_steps(2, 3)

    def export(self):
        now = datetime.now()
        output_path = (OUTPUT_PATH / 'find_plates'
                       / f"output_{now.strftime('%Y-%m-%d_%H-%M-%S')}")
        output_path.mkdir(parents=True, exist_ok=True)
        self._export_images(output_path=output_path)


class ReadPlates(BaseImageProcessing):
    def pre_processing(self, blur_value: int = 35):
        image = self.original_image.copy()
        find_plates = FindPlates(image)
        contours = find_plates.process()
        self.metadata.find_plates = find_plates

        cropped_images = []
        for contour in contours:
            cv2.drawContours(image, contour, -1, (255, 0, 0), 2)
            x, y, w, h = cv2.boundingRect(contour)
            cropped_image = image[y:y + h, x:x + w, :].copy()
            cropped_images.append(cropped_image)

        self.metadata.pre_processing = Munch(cropped_images=cropped_images)
        return cropped_images

    def segmentation(
            self,
            pre_processing,
            lower_thresh_margin: int = 127,
            upper_thresh_margin: int = 255,
            ):
        images_thresh = []
        for cropped_image in pre_processing:
            gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray,
                                      lower_thresh_margin,
                                      upper_thresh_margin,
                                      cv2.THRESH_BINARY_INV)
            images_thresh.append(thresh)

        self.metadata.segmentation = Munch(images_thresh=images_thresh)
        return images_thresh

    def interpretation(self, segmentation, language='por'):
        plates_content = []
        self.metadata.interpretation = Munch(plates_info=Munch())
        plates_info = self.metadata.interpretation.plates_info
        for index, thresh in enumerate(segmentation):
            contours, hierarchy = cv2.findContours(
                    thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            texts_cropped = []
            image_content = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                text_cropped = thresh[y:y + h, x:x + w]
                texts_cropped.append(text_cropped)
                text = pytesseract.image_to_string(text_cropped, lang=language)
                image_content.append(text.strip())

            image_text = ' '.join(image_content)
            plates_content.append(image_content)

            plate_info = Munch(contours=contours,
                               image_content=image_content,
                               image_text=image_text,
                               letters_number=len(image_text.replace(' ', '')),
                               blocks_of_text_number=len(contours))
            setattr(plates_info, str(index), plate_info)

        return plates_content

    def _get_images_data_to_display(self):
        data = self.metadata.find_plates._get_images_data_to_display()
        cropped_images = self.metadata.pre_processing.cropped_images
        for index, image_cropped in enumerate(cropped_images):
            # 6 because the previous was filled by find_plates
            data[f'{6}.{index}-image-cropped'] = image_cropped

        images_thresh = self.metadata.segmentation.images_thresh
        for index, image_thresh in enumerate(images_thresh):
            data[f'{7}.{index}-image-thresh'] = image_thresh

        return data

    def display(self):
        images_data_to_display = self._get_images_data_to_display()
        total_images = len(images_data_to_display)

        columns_tmp = int(total_images / 2)
        while columns_tmp > 5:
            columns_tmp -= 1
        columns = columns_tmp

        rows_tmp = 1
        while columns * rows_tmp <= total_images:
            rows_tmp += 1
        rows = rows_tmp

        self._display_image_processing_steps(
                rows, columns, images_data_to_display)

    def export(self):
        now = datetime.now()
        output_path = (OUTPUT_PATH / 'read_plates'
                       / f"output_{now.strftime('%Y-%m-%d_%H-%M-%S')}")
        output_path.mkdir(parents=True, exist_ok=True)
        self._export_images(output_path=output_path)

        plates_info = self.metadata.interpretation.plates_info
        for label, plate_info in plates_info.items():
            filepath = output_path / f"plate_{label}_text_content.txt"
            with open(filepath, 'wt') as file:
                file.write(plate_info.image_text)
