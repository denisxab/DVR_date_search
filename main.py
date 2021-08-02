import os
import re
from typing import List

import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

# Имя папки с видео файлами
RED_PATH = "D:\mv\Recoverit 2021-07-31 at 21.50.08\Lost Partition 2_1(FAT32)\Lost Location\FRONT\\"

# Папка в которую будут записаны тестовые кадры и найдены совпадения
WRITE_PATH = "test1\\"

Y = 685  # Вертикаль
X = 775  # Горизонталь
H = 300  # высота
W = 330  # ширина


def testCapCaddr():
    """
    Найти нужную область в видео в которой будет распознаваться дата
    """
    global Y, X, H, W
    video_capture = cv2.VideoCapture("{}_ID_001.MOV".format(RED_PATH))
    i = 0
    fps = 3
    while True:
        ret, frame = video_capture.read()
        if ret and fps == 30:
            cv2.imwrite('{}p{}.png'.format(WRITE_PATH, i), frame)
            crop_img = frame[Y:Y + H, X:X + W]
            cv2.imshow("cropped", crop_img)
            cv2.waitKey(0)
            fps = 0
        fps += 1


# @jit(forceobj=True)
def capCaddr(fps_skip=30, required_date: List[str] = None):
    """
    :param fps_skip: Сколько кадров пропускать перед распознаванием даты
    рекомендую ставить 30 либо 60 это будет равно 1 секунде
    """
    global Y, X, H, W

    files = os.listdir(RED_PATH)
    i = 0
    fps = 3
    indexFile = 2
    video_capture = cv2.VideoCapture("{}{}".format(RED_PATH, files[indexFile]))
    print(files[indexFile], indexFile)
    while True:
        ret, frame = video_capture.read()
        if fps == fps_skip:
            if ret:
                res = re.findall(r'[\w]+', pytesseract.image_to_string(frame[Y:Y + H, X:X + W]))
                print(res)
                if required_date == res[:len(required_date)]:
                    print("[TRUE] {}".format(res))
                    cv2.imwrite('{}{}{}{}.png'.format(WRITE_PATH, '_'.join(res),files[indexFile], i), frame)
                i += 1

            else:
                indexFile += 1
                print(files[indexFile], indexFile)
                video_capture = cv2.VideoCapture("{}{}".format(RED_PATH, files[indexFile]))
                print()
            fps = 0

        fps += 1

    print()


if __name__ == '__main__':
    capCaddr(70, ["2020", "07", "30"])
