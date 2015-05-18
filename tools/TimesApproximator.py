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


class TimesApproximator(object):
    def __init__(self):
        self.cap = None
        self.info_file = sys.argv[1].split('.')[0][:-9] + "_info.dat"
        self.times_file = sys.argv[1].split('.')[0] + "_times.dat"

        self.start_time = None
        self.end_time = None
        self.time_diff_mus = None
        self.frame_time_diff_mus = None

        self.frame_count = 0

    def run(self):
        self._check_if_times_file_exists()

        self.cap = cv2.VideoCapture(sys.argv[1])

        print "Frame times approximation started for " + str(sys.argv[1])

        try:
            with open(self.info_file, 'r') as tf:
                self.start_time = datetime.strptime(tf.readline()[12:].rstrip(), '%Y-%m-%d  %H:%M:%S:%f')
                self.end_time = datetime.strptime(tf.readline()[11:].rstrip(), '%Y-%m-%d %H:%M:%S:%f')
        except:
            print "info file missing or badly formatted - can not approximate without start and end time"
            exit()

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
            exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='approximate frametimes for VideoRecorder')
    parser.add_argument('path', type=str, help="absolute file path to VideoRecorder video including file name and file extension")
    
    args = parser.parse_args()
    if not os.path.exists(args.path):
        print('Video file does not exist!')
        exit()

    approx = TimesApproximator()
    approx.run()