#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import math
import sys
import copy
import os
import argparse
import ConfigParser
from ROI import ROI
from DataWriter import DataWriter
from ContourManager import ContourManager
from DataManager import DataManager
from ImageManager import ImageManager
from IPython import embed

class Tracker(object):
    def __init__(self, path=None, nix_io=False, wait_time=50):
        # program data
        self.ui_mode_on = False
        self.ui_abort_button_pressed = False
        
        if path is not None:
            self.video_file = path
        if nix_io:
            try:
                import nix
            except ImportError as e:
                print e
                print 'falling back to text output!'
                nix_io = False

        self.nix_io = nix_io
        self.output_directory = ""
        self.output_path_isset = False
        
        self.cap = None

        self.save_frames = False
        if wait_time > 0:
            self.frame_waittime = wait_time
        else:
            self.frame_waittime = 50

        # self.frame_counter = 0

        # self.__roi = ROI(15, 695, 80, 515)  # Eileen setup
        self._roi = ROI(160, 80, 700, 525)  # Isabel setup

        # image morphing data
        self._erosion_iterations = 1
        self._dilation_iterations = 4

        # fish size thresholds
        self._fish_size_threshold = 700
        self._fish_max_size_threshold = 4000
        self._enable_max_size_threshold = False

        # Managers
        self.cm = ContourManager()
        self.dm = DataManager()
        self.im = ImageManager()

        self.fish_started = False
        self._starting_area_x1_factor = 0.85
        self._starting_area_x2_factor = 1.00
        self._starting_area_y1_factor = 0.30
        self._starting_area_y2_factor = 0.70

        self._start_ori = 270

        self.fish_not_detected_threshold = 50
        self.fish_not_detected_threshold_reached = False

        self.ellipse = None
        # self.line = None

        # import config file values
        self.will_import_config_values = True
        if self.will_import_config_values:
            self.import_config_values()

    def import_config_values(self):
        if not self.will_import_config_values:
            return
        if not os.path.exists('tracker.cnf'):
            print "Couldn't import config data from file - file doesn't exist"
            return

        cfg = ConfigParser.ConfigParser()
        cfg_file = open('tracker.cnf')
        cfg.readfp(cfg_file)

        self._erosion_iterations = cfg.getint('image_morphing', 'erosion_factor')
        self._dilation_iterations = cfg.getint('image_morphing', 'dilation_factor')
        # roi
        self._roi.x1 = cfg.getint('roi', 'x1')
        self._roi.x2 = cfg.getint('roi', 'x2')
        self._roi.y1 = cfg.getint('roi', 'y1')
        self._roi.y2 = cfg.getint('roi', 'y2')

        # starting area
        self.starting_area_x1_factor = cfg.getfloat('starting_area', 'x1_factor')
        self.starting_area_x2_factor = cfg.getfloat('starting_area', 'x2_factor')
        self.starting_area_y1_factor = cfg.getfloat('starting_area', 'y1_factor')
        self.starting_area_y2_factor = cfg.getfloat('starting_area', 'y2_factor')

        self._start_ori = cfg.getint('detection_values', 'start_orientation')
        self._fish_size_threshold = cfg.getint('detection_values', 'min_area_threshold')
        self._fish_max_size_threshold = cfg.getint('detection_values', 'max_area_threshold')
        self._enable_max_size_threshold = cfg.getboolean('detection_values', 'enable_max_size_threshold')

        self.frame_waittime = cfg.getint('system', 'frame_waittime')

        self._erosion_iterations = cfg.getint('image_morphing', 'erosion_factor')
        self._dilation_iterations = cfg.getint('image_morphing', 'dilation_factor')

        self.im.show_bg_sub_img = cfg.getboolean('image_processing', 'show_bg_sub_img')
        self.im.show_morphed_img = cfg.getboolean('image_processing', 'show_morphed_img')
        self.im.draw_contour = cfg.getboolean('image_processing', 'draw_contour')
        self.im.draw_ellipse = cfg.getboolean('image_processing', 'draw_ellipse')

        self.im._lineend_offset = cfg.getint('visualization', 'lineend_offset')
        self.im._circle_size = cfg.getint('visualization', 'circle_size')
        return

    def show_imgs(self, roi_bg_sub, mo_roi_bg_sub):
        if self.im.show_bg_sub_img:
            cv2.imshow("bgsub", roi_bg_sub)
        if self.im.show_morphed_img:
            cv2.imshow("morphed_bgsub", mo_roi_bg_sub)
        return

    # sets video file to terminal-attribute path to video file
    def set_video_file(self):
        if len(sys.argv) > 1:
            self.video_file = sys.argv[1]
        else:
            return

    def set_output_path(self, path):
        self.output_directory = path
        self.output_path_isset = True

    def unset_output_path(self):
        self.output_directory = ""
        self.output_path_isset = False

    def check_if_necessary_files_exist(self):
        if not os.path.exists(self.video_file):
            sys.exit("ERROR: Video File does not exist - Tracking aborted")

    def extract_video_file_name_and_path(self):
        parts = self.video_file.split('/')
        filename = parts[-1].split('.')[0]
        path = '/'.join(parts[:-1])
        if len(path) > 0:
            path += '/'
        return filename, path

    def get_output_file_and_dir(self, file_name, file_directory):
        if not self.output_path_isset:
            output_file_name = file_directory + file_name + "/" + file_name
            out_dir = '/'.join(output_file_name.split('/')[:-1])
            return output_file_name, out_dir
        else:
            output_file_name = self.output_directory + file_name + "/" + file_name
            out_dir = '/'.join(output_file_name.split('/')[:-1])
            return output_file_name, out_dir

    # captures video defined by path stored in video file
    def set_video_capture(self):
        print self.video_file
        self.cap = cv2.VideoCapture(self.video_file)

    # # morph given img by erosion/dilation
    def morph_img(self, img):
        # erode img
        er_kernel = np.ones((4, 4), np.uint8)
        er_img = cv2.erode(img, er_kernel, iterations=self._erosion_iterations)
        # dilate img
        di_kernel = np.ones((4, 4), np.uint8)
        di_img = cv2.dilate(er_img, di_kernel, iterations=self._dilation_iterations)
        # thresholding to black-white
        ret, morphed_img = cv2.threshold(di_img, 127, 255, cv2.THRESH_BINARY)
        # ret, morphed_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        return ret, morphed_img


    # check if fish started from the right side
    def check_if_fish_started(self, roi):
        height, width, depth = roi.shape
        non_starting_area_x1 = int(self._starting_area_x1_factor * width)
        non_starting_area_x2 = int(self._starting_area_x2_factor * width)
        non_starting_area_y1 = int(self._starting_area_y1_factor * height)
        non_starting_area_y2 = int(self._starting_area_y2_factor * height)

        if self.cm.contour_list is not None:
            for i in range(0, len(self.cm.contour_list)):
                cnt = self.cm.contour_list[i]
                ellipse = cv2.fitEllipse(cnt)
                if ellipse[0][0] > non_starting_area_x1 and ellipse[0][0] < non_starting_area_x2 and ellipse[0][1] > non_starting_area_y1 and ellipse[0][1] < non_starting_area_y2:
                    self.fish_started = True

    # fitting ellipse onto contour
    def fit_ellipse_on_contour(self):
        if self.cm.contour_list is None or len(self.cm.contour_list) == 0:
            self.ellipse = None
        elif self.cm.contour_list is not None and len(self.cm.contour_list) > 0:
            if len(self.cm.contour_list) > 0:
                cnt = self.cm.contour_list[0]
                self.ellipse = cv2.fitEllipse(cnt)
                ## center: ellipse[0]
                ## size  : ellipse[1]
                ## angle : ellipse[2]

    def extract_data(self):
        # create BG subtractor
        bg_sub = cv2.BackgroundSubtractorMOG2()

        # main loop
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if frame is None:
                break

            self.dm.frame_counter += 1

            # set region of interest ROI
            roi_img = copy.copy(frame[self.roi.y1:self.roi.y2, self.roi.x1:self.roi.x2])
            roi_output = copy.copy(roi_img)

            self.im.last_frame_ov_output = copy.copy(frame)

            # subtract background fro ROI
            roi_bg_sub = bg_sub.apply(roi_img)

            # morph img
            ret, mo_roi_bg_sub = self.morph_img(roi_bg_sub)

            # getting contours (of the morphed img)
            ret, thresh_img = cv2.threshold(mo_roi_bg_sub, 127, 255, cv2.THRESH_BINARY)
            self.cm.contour_list, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            # save amount of contours
            self.dm.save_number_of_contours(self.cm.contour_list, self.dm.number_contours_per_frame)

            # everything below fish_size_threshold is being ignored
            self.cm.del_small_contours(self.fish_size_threshold)

            # everything above fish_size_max_threshold is being ignored
            if self._enable_max_size_threshold:
                self.cm.del_oversized_contours(self.fish_max_size_threshold)

            # save number of remaining contours
            self.dm.save_number_of_contours(self.cm.contour_list, self.dm.number_relevant_contours_per_frame)

            # check if fish started
            if not self.fish_started:
                self.check_if_fish_started(roi_img)

            # if fish hasn't started yet, delete all contours
            if not self.fish_started:
                self.cm.contour_list = []

            # keep only biggest contours
            self.cm.keep_biggest_contours()

            # if two or more contours (of same size) in list delete which is farthest away from last point
            if self.fish_started and self.cm.contour_list is not None and len(self.cm.contour_list) > 1:
                self.cm.keep_nearest_contour(self.dm.last_pos, self.ellipse, self.roi)

            # fit ellipse on contour
            self.fit_ellipse_on_contour()

            # get line from ellipse
            if self.fish_started and self.ellipse is not None:
                self.im.get_line_from_ellipse(self.ellipse)

            # append ellipse center to travel route
            if self.im.draw_travel_route:
                self.im.append_to_travel_route(self.ellipse)

            # set last_pos to ellipse center
            self.dm.set_last_pos(self.ellipse)

            # save fish positions
            self.dm.save_fish_positions(self.roi)

            # set last orientation
            self.dm.set_last_orientation(self.ellipse, self.fish_started, self.start_ori)

            # save orientations
            self.dm.save_fish_orientations(self.ellipse, self.fish_started)

            # append coordinates to travel_orientation
            if self.im.draw_travel_orientation and self.fish_started:
                self.im.append_to_travel_orientation()

            self.im.draw_extracted_data(self.ellipse, self.fish_started, roi_img, self.cm.contour_list)
            self.im.draw_data_on_overview_image(self.roi, self.dm)

            # show all imgs
            self.show_imgs(roi_bg_sub, mo_roi_bg_sub)

            # show output img
            if not self.ui_mode_on:
                cv2.imshow("contours", roi_img)

            self.im.last_frame = roi_img
            # self.im.last_frame_ov_output = frame_output
            if cv2.waitKey(self.frame_waittime) & 0xFF == 27:
                break
            if self.ui_abort_button_pressed:
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def load_frame_times(self, file_name):
        times_file = None
        if not os.path.exists(file_name):
            sys.exit("ERROR: times file missing - data saving abortet")
        
        with open(file_name, 'r') as f:
            times = map(lambda x: x.strip(), f)
        return times


        
    def run(self):
        self.set_video_file()
        self.check_if_necessary_files_exist()
        self.set_video_capture()

        self.extract_data()
        self.dm.estimate_missing_pos(self.roi)
        self.dm.estimate_missing_ori()
        self.im.draw_estimated_data(self.dm.estimated_pos_roi, self.roi, self.im.circle_size)

        self.dm.copy_original_to_est_data()

        # self.print_data()
        self.dm.check_frames_missing_fish(self.fish_not_detected_threshold)

        file_name, file_directory = self.extract_video_file_name_and_path()
        if file_name == "":
            return

        times = self.load_frame_times(file_directory + file_name + "_times.dat")
        output_file_name, out_dir = self.get_output_file_and_dir(file_name, file_directory)

        params = {}
        params['fish size'] = self._fish_size_threshold
        params['start ori'] = self._start_ori
        params['starting area x1'] = self._starting_area_x1_factor
        params['starting area x2'] = self._starting_area_x2_factor
        params['starting area y1'] = self._starting_area_y1_factor
        params['starting area y2'] = self._starting_area_y2_factor
        params['source file'] = self.video_file

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        if not self.nix_io:
            DataWriter.write_ascii(output_file_name + ".txt", times, self.dm.all_pos_original, self.dm.all_oris,
                                   self.dm.estimated_pos_original, self.dm.estimated_oris, self.dm.number_contours_per_frame,
                                   self.dm.number_relevant_contours_per_frame, self.roi, self.dm.frame_counter, params)
        else:
            DataWriter.write_nix(output_file_name + ".h5", times, self.dm.all_pos_original, self.dm.all_oris,
                                 self.dm.estimated_pos_original, self.dm.estimated_oris, self.dm.number_contours_per_frame,
                                 self.dm.number_relevant_contours_per_frame, self.roi, params)
        cv2.imwrite(output_file_name + "_OV_path.png", self.im.last_frame_ov_output)

        self.dm.check_data_integrity()

    @property
    def roi(self):
        return self._roi

    @property
    def erosion_iterations(self):
        return self._erosion_iterations

    @erosion_iterations.setter
    def erosion_iterations(self, value):
        self._erosion_iterations = value

    @property
    def dilation_iterations(self):
        return self._dilation_iterations

    @dilation_iterations.setter
    def dilation_iterations(self, value):
        self._dilation_iterations = value

    @property
    def fish_size_threshold(self):
        return self._fish_size_threshold

    @fish_size_threshold.setter
    def fish_size_threshold(self, value):
        self._fish_size_threshold = value
        self.cm.fish_max_size_threshold = self.fish_size_threshold

    @property
    def fish_max_size_threshold(self):
        return self._fish_max_size_threshold

    @fish_max_size_threshold.setter
    def fish_max_size_threshold(self, value):
        self._fish_max_size_threshold = value
        self.cm.fish_max_size_threshold = self.fish_max_size_threshold

    @property
    def enable_max_size_threshold(self):
        return self._enable_max_size_threshold

    @enable_max_size_threshold.setter
    def enable_max_size_threshold(self, bool):
        self._enable_max_size_threshold = bool

    @property
    def starting_area_x1_factor(self):
        return self._starting_area_x1_factor

    @starting_area_x1_factor.setter
    def starting_area_x1_factor(self, value):
        self._starting_area_x1_factor = value

    @property
    def starting_area_x2_factor(self):
        return self._starting_area_x2_factor

    @starting_area_x2_factor.setter
    def starting_area_x2_factor(self, value):
        self._starting_area_x2_factor = value

    @property
    def starting_area_y1_factor(self):
        return self._starting_area_y1_factor

    @starting_area_y1_factor.setter
    def starting_area_y1_factor(self, value):
        self._starting_area_y1_factor = value

    @property
    def starting_area_y2_factor(self):
        return self._starting_area_y2_factor

    @starting_area_y2_factor.setter
    def starting_area_y2_factor(self, value):
        self._starting_area_y2_factor = value

    @property
    def start_ori(self):
        return self._start_ori

    @start_ori.setter
    def start_ori(self, value):
        self._start_ori = value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tracking fish in video file')
    parser.add_argument('path', type=str, help="absolute file path to video including file name and file extension")
    parser.add_argument('-n', '--nix_output', type=bool, default=False,
                        help="output tracking results to nix file")
    parser.add_argument('-w', '--wait_time', type=int, default=50,
                        help="display time of wach frame in ms.")
    
    args = parser.parse_args()
    if not os.path.exists(args.path):
        print('File does not exist!')
        exit()
    tr = Tracker(args.path, args.nix_output, args.wait_time)
    tr.run()
