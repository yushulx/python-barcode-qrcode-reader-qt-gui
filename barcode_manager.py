
from dbr import *
import cv2
from multiprocessing import Process, Queue
import time
import numpy as np


def process_barcode_frame(license, frameQueue, resultQueue):
    # Create Dynamsoft Barcode Reader
    reader = BarcodeReader()
    # Apply for a trial license: https://www.dynamsoft.com/customer/license/trialLicense
    reader.init_license(license)
    settings = reader.get_runtime_settings()
    settings.max_algorithm_thread_count = 1
    reader.update_runtime_settings(settings)

    while True:
        results = None

        try:
            frame = frameQueue.get(False, 10)
            if type(frame) is str:
                break
        except:
            time.sleep(0.01)
            continue

        try:
            frameHeight, frameWidth, channel = frame.shape[:3]
            # results = reader.decode_buffer(frame)
            results = reader.decode_buffer_manually(np.array(frame).tobytes(), frameWidth, frameHeight, frame.strides[0], EnumImagePixelFormat.IPF_RGB_888)
        except BarcodeReaderError as error:
            print(error)

        try:
            resultQueue.put(results, False, 10)
        except:
            pass

def create_decoding_process(license):
        size = 1
        frameQueue = Queue(size)
        resultQueue = Queue(size)
        barcodeScanning = Process(target=process_barcode_frame, args=(license, frameQueue, resultQueue))
        barcodeScanning.start()
        return frameQueue, resultQueue, barcodeScanning

class BarcodeManager():
    def __init__(self, license):
        self._reader = BarcodeReader()
        self._reader.init_license(license)
        settings = self._reader.get_runtime_settings()
        settings.max_algorithm_thread_count = 1
        self._reader.update_runtime_settings(settings)

    def __decode_buffer(self, frame):
        if frame is None:
            return None, ''
        results = self._reader.decode_buffer(frame)
        out = ''
        index = 0
        
        if results is not None:
            thickness = 2
            color = (0,255,0)
            for result in results:
                out += "Index: " + str(index) + "\n"
                out += "Barcode format: " + result.barcode_format_string + '\n'
                out += "Barcode value: " + result.barcode_text + '\n'
                out += '-----------------------------------\n'
                index += 1

                points = result.localization_result.localization_points

                cv2.line(frame, points[0], points[1], color, thickness)
                cv2.line(frame, points[1], points[2], color, thickness)
                cv2.line(frame, points[2], points[3], color, thickness)
                cv2.line(frame, points[3], points[0], color, thickness)
                cv2.putText(frame, result.barcode_text, points[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))

        return frame, out

    def decode_frame(self, frame):
        return self.__decode_buffer(frame)

    def decode_file(self, filename):
        frame = cv2.imread(filename)
        return self.__decode_buffer(frame)

    

    