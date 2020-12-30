
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
            return None, None

        
        results = self._reader.decode_buffer(frame)
        return frame, results

    def decode_frame(self, frame):
        return self.__decode_buffer(frame)

    def decode_file(self, filename):
        frame = cv2.imread(filename)
        return self.__decode_buffer(frame)

    def set_template(self, template):
        self.template = template

    def set_barcode_types(self, types):
        self.types = types

    

    