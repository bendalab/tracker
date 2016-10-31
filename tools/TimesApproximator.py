#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
For starters coded for files created by videoRecorder
"""

import numpy as np
from datetime import datetime
from datetime import timedelta
import cv2
import math
import sys
import copy
import os
import argparse
from IPython import embed

class TimesApproximator(object):
    def __init__(self, path):
        self.cap = None
        path_stub = os.path.sep.join(path.split(os.path.sep)[:-1])
        info_temp = '_'.join(path.split(os.path.sep)[-1].split('.')[0].split('_')[:2]) + "_info.dat"    
        self.info_file = os.path.sep.join([path_stub, info_temp])
        self.times_file = os.path.sep.join([path_stub, '_'.join(path.split(os.path.sep)[-1].split('.')[0].split('_')[:2]) + "_times.dat" ])

        self.start_time = None
        self.end_time = None
        self.time_diff_mus = None
        self.frame_time_diff_mus = None

        self.frame_count = 0

    def run(self, path):
        print "Frame times approximation started for " + str(path)

        if self._check_if_times_file_exists():
            return

        self.cap = cv2.VideoCapture(path)

        try:
            with open(self.info_file, 'r') as tf:
                self.start_time = datetime.strptime(tf.readline()[12:].rstrip(), '%Y-%m-%d  %H:%M:%S:%f')
                self.end_time = datetime.strptime(tf.readline()[11:].rstrip(), '%Y-%m-%d %H:%M:%S:%f')
        except:
            print "info file missing or badly formatted - can not approximate without start and end time"
            return

        self._get_time_diff()
        self._count_frames()
        self._calculate_frame_time_diff()
        self._write_times_file()

    def _get_time_diff(self):
        time_diff = self.end_time - self.start_time
        self.time_diff_mus = time_diff.seconds*1000000 + time_diff.microseconds

    def _count_frames(self):
        while self.cap.isOpened():
            self.frame_count += 1

            ret, frame = self.cap.read()

            if frame is None:
                break

        self.cap.release()

    def _calculate_frame_time_diff(self):
        self.frame_time_diff_mus = int(self.time_diff_mus/self.frame_count)

    def _write_times_file(self):
        printtime = datetime.strptime('00:00:00:000000', '%H:%M:%S:%f')
        addtime = timedelta(0, 0, self.frame_time_diff_mus)

        with open(self.times_file, 'a') as tf:
            for i in range(self.frame_count + 1):
                tf.write(str(printtime)[11:] + "\n")
                printtime = printtime + addtime

    def _check_if_times_file_exists(self):
        if os.path.exists(self.times_file):
            print "Times File already exists! If you want to create a new Times File please delete the old one.\nApproximation aborted"
            return True
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='approximate frametimes for VideoRecorder')
    parser.add_argument('path', type=str, nargs="*", help="absolute file path to VideoRecorder video including file name and file extension")
    
    args = parser.parse_args()

    for path in args.path:
        if not os.path.exists(path):
            print('Video file does not exist!')
            continue

        approx = TimesApproximator(path)
        approx.run(path)
