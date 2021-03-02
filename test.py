#!/usr/bin/env python3

'''
Usage:
   test.py <image file>
'''

from dbr import *
from PySide2.QtWidgets import QApplication, QMainWindow, QInputDialog
import cv2


def main():
    try:
        file_path = sys.argv[1]
    except:
        print(__doc__)
        return

    image = cv2.imread(file_path)
    reader = BarcodeReader()
    try:
        text_results = reader.decode_buffer(image)
        if text_results != None:
            for text_result in text_results:
                print("Barcode Format : ")
                print(text_result.barcode_format_string)
                print("Barcode Text : ")
                print(text_result.barcode_text)
                print("Localization Points : ")
                print(text_result.localization_result.localization_points)
                print("Exception : ")
                print(text_result.exception)
                print("-------------")
    except BarcodeReaderError as bre:
        print(bre)

    app = QApplication(sys.argv)
    print('Quit the app.')


if __name__ == '__main__':
    main()