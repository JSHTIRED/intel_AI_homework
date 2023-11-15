# !/usr/bin/env python3

from openvino.inference_engine import IECore
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep
import os
# pylint: disable=no-member
import cv2
import numpy as np
from iotdemo import MotionDetector
from iotdemo import FactoryController
from iotdemo import ColorDetector

FORCE_STOP = False


def thread_cam1(q):
    # pylint: disable=missing-function-docstring
    # 함수의 본문
    #  MotionDetector
    det = MotionDetector()
    det.load_preset("resources/motion.cfg", "default")
    #  Load and initialize OpenVINO
    color = ColorDetector()
    color.load_preset("resources/color.cfg", "default")
    
    # HW2 Open video clip resources/conveyor.mp4 instead of camera device.
    video_path = os.path.abspath("resources/conveyor.mp4")
    cap = cv2.VideoCapture(video_path)

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        #  HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put(("VIDEO:Cam1 live", frame))

        #  Motion detect
        
        detected = det.detect(frame)
        if detected is None:
            continue

        # nqueue "VIDEO:Cam1 detected", detected info.
        q.put(("VIDEO:Cam1 detected", detected))

        # abnormal detect
        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        reshaped = detected[:, :, [2, 1, 0]]
        np_data = np.moveaxis(reshaped, -1, 0)
        preprocessed_numpy = [((np_data / 255.0) - 0.5) * 2]
        batch_tensor = np.stack(preprocessed_numpy, axis=0)
        """
        #  Inference OpenVINO
      
        predict = color.detect(frame)
        if not predict:
            continue
        # TODO: Calculate ratios
        name, ratio = predict[0]
        ratio = ratio*100
        print(f"{name}: {ratio:.2f}%")

        # TODO: in queue for moving the actuator 1
        q.put(("PUSH", 1))

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q):
    # pylint: disable=missing-function-docstring
    # MotionDetector
    det = MotionDetector()
    det.load_preset("resources/motion.cfg", "default")

    # ColorDetector
    color = ColorDetector()
    color.load_preset("resources/color.cfg", "default")    
    # HW2 Open "resources/conveyor.mp4" video clip
    cap = cv2.VideoCapture("resources/conveyor.mp4")
    
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # HW2 Enqueue "VIDEO:Cam2 live", frame info
        q.put(("VIDEO:Cam2 live", frame))

        # Detect motion
        detected = det.detect(frame)
        if detected is None:
            continue

        # Enqueue "VIDEO:Cam2 detected", detected info.
        q.put(("VIDEO:Cam2 detected", detected))

        # Detect color
       
        predict = color.detect(frame)
        if not predict:
            continue
       
        # Compute ratio
        name, ratio = predict[0]
        ratio = ratio*100

        print(f"{name}: {ratio:.2f}%")

        # Enqueue to handle actuator 2
        q.put(("PUSH", 2))

    cap.release()
    q.put(('DONE', None))
    exit()


def imshow(title, frame, pos=None):
    # pylint: disable=missing-function-docstring
    cv2.namedWindow(title)
    if pos:
        cv2.moveWindow(title, pos[0], pos[1])
    cv2.imshow(title, frame)


def main():
    # pylint: disable=missing-function-docstring
    # pylint: disable=global-statement
    global FORCE_STOP  
    # 모듈 수준에서 초기화
    parser = ArgumentParser(prog='python3 factory.py',
                            description="Factory tool")

    parser.add_argument("-d",
                        "--device",
                        default=None,
                        type=str,
                        help="Arduino port")
    args = parser.parse_args()

    # HW2 Create a Queue
    q = Queue()

    # HW2 Create thread_cam1 and thread_cam2 threads and start them.
    t1 = threading.Thread(target=thread_cam1, args=(q, ))
    t2 = threading.Thread(target=thread_cam2, args=(q, ))

    t1.start()
    t2.start()

    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            key = cv2.waitKey(10)
            if key & 0xff == ord('q'):
                FORCE_STOP = True
            # HW2 get an item from the queue.
            # You might need to properly handle exceptions.
            # de-queue name and data
            
            try:
                e = q.get_nowait()
            except Empty:
                continue

            name, frame = e
            if name.startswith("VIDEO:"):
                imshow(name[6:], frame)
            elif name == "PUSH":
                ctrl.push_actuator(frame)
            elif name == "none":
                FORCE_STOP = True
            q.task_done()

    t1.join()
    t2.join()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
    
        
