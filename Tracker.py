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
        
        self.cap = ""

        self.save_frames = False
        if wait_time > 0:
            self.frame_waittime = wait_time
        else:
            self.frame_waittime = 50

        self.frame_counter = 0

        # self.__roi = ROI(15, 695, 80, 515) # Eileen setup
        self._roi = ROI(160, 80, 700, 525) # Isabel setup

        # image morphing data
        self._erosion_iterations = 1
        self._dilation_iterations = 4


        # fish size thresholds
        self._fish_size_threshold = 700
        self._fish_max_size_threshold = 4000
        self._enable_max_size_threshold = False

        # tracking data
        self.cm = ContourManager()

        self.fish_started = False
        self._starting_area_x1_factor = 0.85
        self._starting_area_x2_factor = 1.00
        self._starting_area_y1_factor = 0.30
        self._starting_area_y2_factor = 0.70

        self.last_pos = None
        self.all_pos_roi = []
        self.all_pos_original = []

        self.last_ori = None
        self._start_ori = 270
        self.all_oris = []

        self.fish_not_detected_count = 0
        self.fish_not_detected_threshold = 50
        self.fish_not_detected_threshold_reached = False

        self.ellipse = None
        self.line = None
        self._lineend_offset = 5
        self._circle_size = 2
        self.lx1 = 0
        self.ly1 = 0
        self.lx2 = 0
        self.ly2 = 0

        self.img_travel_orientation = []
        self.img_travel_route = []

        self.number_contours_per_frame = []
        self.number_relevant_contours_per_frame = []

        self.last_frame = None
        self.last_frame_OV_output = None

        # img output
        self._draw_contour = False
        self._draw_ellipse = True
        self.draw_line = True
        self.draw_travel_orientation = True
        self.draw_travel_route = True
        self.draw_original_output = True
        self._show_bg_sub_img = False
        self._show_morphed_img = False

        self.estimate_missing_data = True
        self.estimated_pos_roi = []
        self.estimated_pos_original = []
        self.estimated_oris = []

        # import config file values
        self.will_import_config_values = True
        if self.will_import_config_values:
            self.import_config_values()

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

    @property
    def lineend_offset(self):
        return self._lineend_offset

    @lineend_offset.setter
    def lineend_offset(self, value):
        self._lineend_offset = value

    @property
    def circle_size(self):
        return self._circle_size

    @circle_size.setter
    def circle_size(self, value):
        self._circle_size = value

    @property
    def draw_contour(self):
        return self._draw_contour

    @draw_contour.setter
    def draw_contour(self, boo):
        self._draw_contour = boo

    @property
    def draw_ellipse(self):
        return self._draw_ellipse

    @draw_ellipse.setter
    def draw_ellipse(self, boo):
        self._draw_ellipse = boo

    @property
    def show_bg_sub_img(self):
        return self._show_bg_sub_img

    @show_bg_sub_img.setter
    def show_bg_sub_img(self, boo):
        self._show_bg_sub_img = boo

    @property
    def show_morphed_img(self):
        return self._show_bg_sub_img

    @show_morphed_img.setter
    def show_morphed_img(self, boo):
        self._show_morphed_img = boo


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

        self._show_bg_sub_img = cfg.getboolean('image_processing', 'show_bg_sub_img')
        self._show_morphed_img = cfg.getboolean('image_processing', 'show_morphed_img')
        self._draw_contour = cfg.getboolean('image_processing', 'draw_contour')
        self._draw_ellipse = cfg.getboolean('image_processing', 'draw_ellipse')

        self._lineend_offset = cfg.getint('visualization', 'lineend_offset')
        self._circle_size = cfg.getint('visualization', 'circle_size')
        return

    def show_imgs(self, img, roi_output, roi_bg_sub, mo_roi_bg_sub, edges):
        if self._show_bg_sub_img:
            cv2.imshow("bgsub", roi_bg_sub)
        if self._show_morphed_img:
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

    @staticmethod
    def save_number_of_contours(cnt_list, number_cnt_list):
        if cnt_list is None:
            number_cnt_list.append(0)
        else:
            number_cnt_list.append(len(cnt_list))

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

    # calculates start and endpoint for a line displaying the orientation of given ellipse (thus of the fish)
    def get_line_from_ellipse(self):
        center_x = self.ellipse[0][0]
        center_y = self.ellipse[0][1]
        grade_angle = -1 * self.ellipse[2]
        angle_prop = grade_angle/180
        angle = math.pi*angle_prop

        x_dif = math.sin(angle)
        y_dif = math.cos(angle)

        x1 = int(round(center_x - self._lineend_offset*x_dif))
        y1 = int(round(center_y - self._lineend_offset*y_dif))
        x2 = int(round(center_x + self._lineend_offset*x_dif))
        y2 = int(round(center_y + self._lineend_offset*y_dif))

        return x1, y1, x2, y2

    def append_to_travel_orientation(self):
        coordinates = (self.lx1, self.ly1, self.lx2, self.ly2)
        self.img_travel_orientation.append(coordinates)

    def append_to_travel_route(self):
        if self.ellipse is not None:
            ellipse_x = int(round(self.ellipse[0][0]))
            ellipse_y = int(round(self.ellipse[0][1]))
            point = (ellipse_x, ellipse_y)
            self.img_travel_route.append(point)

    def set_last_pos(self):
        if self.ellipse is None:
            self.last_pos = None
            return
        else:
            self.last_pos = self.ellipse[0]

    def save_fish_positions(self):
        self.all_pos_roi.append(self.last_pos)
        if self.last_pos is None:
            self.all_pos_original.append(self.last_pos)
        else:
            original_x = self.last_pos[0] + self.roi.x1
            original_y = self.last_pos[1] + self.roi.y1
            self.all_pos_original.append((original_x, original_y))

    def set_last_orientation(self):
        if not self.fish_started or self.ellipse is None:
            return

        if self.last_ori is None:
            self.last_ori = self._start_ori

        if self.ellipse is None:
            return

        ell_ori = self.ellipse[2]
        if self.last_ori > ell_ori:
            ori_diff = self.last_ori - ell_ori
            if ori_diff > 270:
                self.last_ori = ell_ori
            elif ori_diff < 90:
                self.last_ori = ell_ori
            else:
                self.last_ori = (ell_ori + 180) % 360
        if self.last_ori < ell_ori:
            ori_diff = ell_ori - self.last_ori
            if ori_diff < 90:
                self.last_ori = ell_ori
            else:
                self.last_ori = (ell_ori + 180) % 360

    def save_fish_orientations(self):
        if not self.fish_started:
            self.all_oris.append(None)
            return

        if self.ellipse is None:
            self.all_oris.append(None)
            return

        self.all_oris.append(self.last_ori)

    def estimate_missing_pos(self):
        if not self.estimate_missing_data:
            return

        global frame_counter
        global all_pos_roi
        global estimated_pos_roi
        global estimated_pos_original
        global ROI_X1
        global ROI_Y1

        # init length of estimated-lists to amount of frames
        for x in range(0, self.frame_counter):
            self.estimated_pos_roi.append(None)
            self.estimated_pos_original.append(None)

        # set pointer to start of data
        pointer = 0
        while pointer < self.frame_counter and self.all_pos_roi[pointer] is None:
            pointer += 1

        while pointer < self.frame_counter:
            while self.all_pos_roi[pointer] is not None:
                pointer += 1
                if pointer >= self.frame_counter-1:
                    return

            gap_start_pointer = pointer
            gap_end_pointer = pointer
            while gap_end_pointer < self.frame_counter-1 and self.all_pos_roi[gap_end_pointer] is None:
                gap_end_pointer += 1

            if gap_end_pointer == self.frame_counter-1:
                break

            start_value_x = self.all_pos_roi[gap_start_pointer-1][0]
            start_value_y = self.all_pos_roi[gap_start_pointer-1][1]
            end_value_x = self.all_pos_roi[gap_end_pointer][0]
            end_value_y = self.all_pos_roi[gap_end_pointer][1]

            pointer_diff = gap_end_pointer - (gap_start_pointer-1)
            value_diff_x = end_value_x - start_value_x
            value_diff_y = end_value_y - start_value_y
            value_diff_x_part = value_diff_x/pointer_diff
            value_diff_y_part = value_diff_y/pointer_diff


            # print "pointer diff = " + str(pointer_diff)
            first_pos_estimated = False
            while pointer < gap_end_pointer:
                if not first_pos_estimated:
                    self.estimated_pos_roi[pointer] = ((self.all_pos_roi[pointer-1][0] + value_diff_x_part), (self.all_pos_roi[pointer-1][1] + value_diff_y_part))
                    self.estimated_pos_original[pointer] = (self.estimated_pos_roi[pointer][0] + self.roi.x1, self.estimated_pos_roi[pointer][1] + self.roi.y1)
                    first_pos_estimated = True
                else:
                    self.estimated_pos_roi[pointer] = ((self.estimated_pos_roi[pointer-1][0] + value_diff_x_part), (self.estimated_pos_roi[pointer-1][1] + value_diff_y_part))
                    self.estimated_pos_original[pointer] = (self.estimated_pos_roi[pointer][0] + self.roi.x1, self.estimated_pos_roi[pointer][1] + self.roi.y1)
                pointer += 1

    def estimate_missing_ori(self):
        if self.frame_counter < 1:
            return

        # init length of estimated-list to amount of frames
        for x in range(0, self.frame_counter):
            self.estimated_oris.append(None)

        pointer = 0
        # set pointer to start of data
        while self.all_oris[pointer] is None:
            pointer += 1
            if pointer >= self.frame_counter-1:
                    return

        while pointer < self.frame_counter:
            while self.all_oris[pointer] is not None:
                pointer += 1
                if pointer >= self.frame_counter-1:
                    return

            gap_start_pointer = pointer
            gap_end_pointer = pointer
            while gap_end_pointer < self.frame_counter-1 and self.all_oris[gap_end_pointer] is None:
                gap_end_pointer += 1

            if gap_end_pointer == self.frame_counter-1:
                break

            start_value = self.all_oris[gap_start_pointer-1]
            end_value = self.all_oris[gap_end_pointer]

            pointer_diff = gap_end_pointer - (gap_start_pointer-1)
            value_diff = end_value - start_value
            if start_value > end_value and abs(value_diff) > 180:
                value_diff = (end_value + 360) - start_value
            elif start_value < end_value and abs(value_diff) > 180:
                value_diff = (end_value - 360) - start_value
            value_diff_part = value_diff/pointer_diff

            first_pos_estimated = False
            while pointer < gap_end_pointer:
                if not first_pos_estimated:
                    self.estimated_oris[pointer] = (self.all_oris[pointer-1] + value_diff_part) % 360
                    first_pos_estimated = True
                else:
                    self.estimated_oris[pointer] = (self.estimated_oris[pointer-1] + value_diff_part) % 360
                pointer += 1

    def draw_estimated_data(self):
        if not self.estimate_missing_data:
            return

        for c in self.estimated_pos_roi:
            if c is not None:
                cv2.circle(self.last_frame, (int(round(c[0])), int(round(c[1]))), self._circle_size, (0, 0, 255))
                cv2.circle(self.last_frame_OV_output, (int(round(c[0])) + self.roi.x1, int(round(c[1]) + self.roi.y1)), self._circle_size, (0, 0, 255))

    def copy_original_to_est_data(self):
        for i in range(0, self.frame_counter):
            if self.all_pos_roi[i] is not None:
                self.estimated_pos_roi[i] = self.all_pos_roi[i]
            if self.all_pos_original[i] is not None:
                self.estimated_pos_original[i] = self.all_pos_original[i]
            if self.all_oris[i] is not None:
                self.estimated_oris[i] = self.all_oris[i]

    def extract_data(self):
        # create BG subtractor
        bg_sub = cv2.BackgroundSubtractorMOG2()

        # main loop
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if frame is None:
                break

            self.frame_counter += 1

            # set region of interest ROI
            roi = copy.copy(frame[self.roi.y1:self.roi.y2, self.roi.x1:self.roi.x2])
            roi_output = copy.copy(roi)

            frame_output = copy.copy(frame)

            # subtract background fro ROI
            roi_bg_sub = bg_sub.apply(roi)

            # morph img
            ret, mo_roi_bg_sub = self.morph_img(roi_bg_sub)

            # detect edges of bg-deleted img
            edges = cv2.Canny(mo_roi_bg_sub, 500, 500)

            # detect edges of morphed img (not displayed)
            mo_edges = cv2.Canny(mo_roi_bg_sub, 500, 500)

            # getting contours (of the morphed img)
            ret, thresh_img = cv2.threshold(mo_roi_bg_sub, 127, 255, cv2.THRESH_BINARY)
            self.cm.contour_list, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            # save amount of contours
            self.save_number_of_contours(self.cm.contour_list, self.number_contours_per_frame)

            # everything below fish_size_threshold is being ignored
            self.cm.del_small_contours(self.fish_size_threshold)

            # everything above fish_size_max_threshold is being ignored
            if self._enable_max_size_threshold:
                self.cm.del_oversized_contours(self.fish_max_size_threshold)

            # save number of remaining contours
            self.save_number_of_contours(self.cm.contour_list, self.number_relevant_contours_per_frame)

            # check if fish started
            if not self.fish_started:
                self.check_if_fish_started(roi)

            # if fish hasn't started yet, delete all contours
            if not self.fish_started:
                self.cm.contour_list = []

            # keep only biggest contours
            self.cm.keep_biggest_contours()

            # if two or more contours (of same size) in list delete which is farthest away from last point
            if self.fish_started and self.cm.contour_list is not None and len(self.cm.contour_list) > 1:
                self.cm.keep_nearest_contour(self.last_pos, self.ellipse, self.roi)

            # draw countours to ROI img and show img
            if self.draw_contour:
                cv2.drawContours(roi, self.cm.contour_list, -1, (0, 255, 0), 3)

            # fit ellipse on contour
            self.fit_ellipse_on_contour()
            # draw ellipse
            if self._draw_ellipse and self.ellipse is not None and self.fish_started:
                cv2.ellipse(roi, self.ellipse, (0, 0, 255), 2)

            # get line from ellipse
            if self.fish_started and self.ellipse is not None:
                self.lx1, self.ly1, self.lx2, self.ly2 = self.get_line_from_ellipse()
            # draw line
            if self.draw_line and self.ellipse is not None:
                cv2.line(roi, (self.lx1, self.ly1), (self.lx2, self.ly2), (0, 0, 255), 1)

            # append ellipse center to travel route
            if self.draw_travel_route:
                self.append_to_travel_route()

            # set last_pos to ellipse center
            self.set_last_pos()

            # save fish positions
            self.save_fish_positions()

            # set last orientation
            self.set_last_orientation()

            # save orientations
            self.save_fish_orientations()

            # append coordinates to travel_orientation
            if self.draw_travel_orientation and self.fish_started:
                self.append_to_travel_orientation()


            # draw travel route
            if self.draw_travel_orientation:
                for coordinates in self.img_travel_orientation:
                    cv2.line(roi, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), (150,150,0), 1)

            # draw travel orientation
            if self.draw_travel_route:
                for point in self.img_travel_route:
                    cv2.circle(roi, point, self._circle_size, (255, 0, 0))

            if self.draw_original_output:
                for coordinates in self.img_travel_orientation:
                    cv2.line(frame_output, (coordinates[0] + self.roi.x1, coordinates[1] + self.roi.y1), 
                             (coordinates[2] + self.roi.x1, coordinates[3] + self.roi.y1), (150,150,0), 1)
                for point in self.all_pos_original:
                    if point is not None:
                        cv2.circle(frame_output, (int(round(point[0])), int(round(point[1]))), self._circle_size, (255, 0, 0))

            # show all imgs
            if self.draw_original_output:
                self.show_imgs(frame_output, roi_output, roi_bg_sub, mo_roi_bg_sub, edges)
            else:
                self.show_imgs(frame, roi_output, roi_bg_sub, mo_roi_bg_sub, edges)

            # show output img
            if not self.ui_mode_on:
                cv2.imshow("contours", roi)
            # if SAVE_FRAMES:
            #     cv2.imwrite(dir + "frames/" + str(frame_counter) + "_contours" + ".jpg", roi)

            self.last_frame = roi
            self.last_frame_OV_output = frame_output
            if cv2.waitKey(self.frame_waittime) & 0xFF == 27:
                break
            if self.ui_abort_button_pressed:
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def print_data(self):
        print "positions region of interest: " + str(self.all_pos_roi)
        print "estimated positions roi:      " + str(self.estimated_pos_roi)
        print "positions original recording: " + str(self.all_pos_original)
        print "estimated positions original: " + str(self.estimated_pos_original)
        print "all orientations:             " + str(self.all_oris)
        print "estimated orientations:       " + str(self.estimated_oris)
        print "number of contours in frames: " + str(self.number_contours_per_frame)
        print "number of fish-size contours: " + str(self.number_relevant_contours_per_frame)

    def check_data_integrity(self):
        if not len(self.all_pos_roi) == len(self.all_pos_original) == len(self.all_oris) == self.frame_counter:
            print "WARNING: Something went wrong. Length of Lists saving fish data not consistent with frame count!"

        print "All lists consistent with frame count: " + str(len(self.all_pos_roi) == len(self.all_pos_original) == len(self.all_oris) == len(self.number_contours_per_frame) == len(self.number_relevant_contours_per_frame) == self.frame_counter)

    def check_frames_missing_fish(self):
        startPos = 0
        for entry in self.all_oris:
            if entry is None:
                startPos += 1

        for i in range(startPos, len(self.all_oris), 1):
            if self.all_oris[i] is None:
                self.fish_not_detected_count += 1

        if self.fish_not_detected_count > self.fish_not_detected_threshold:
            self.fish_not_detected_threshold_reached = True

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
        self.estimate_missing_pos()
        self.estimate_missing_ori()
        self.draw_estimated_data()

        self.copy_original_to_est_data()

        # self.print_data()
        self.check_frames_missing_fish()

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
            DataWriter.write_ascii(output_file_name + ".txt", times, self.all_pos_original, self.all_oris,
                                   self.estimated_pos_original, self.estimated_oris, self.number_contours_per_frame, 
                                   self.number_relevant_contours_per_frame, self.roi, self.frame_counter, params)
        else:
            DataWriter.write_nix(output_file_name + ".h5", times, self.all_pos_original, self.all_oris, 
                                 self.estimated_pos_original, self.estimated_oris, self.number_contours_per_frame, 
                                 self.number_relevant_contours_per_frame, self.roi, params)
        cv2.imwrite(output_file_name + "_OV_path.png", self.last_frame_OV_output)

        self.check_data_integrity()

        # if self.draw_original_output:
        #     cv2.namedWindow("result_ov")
        #     cv2.moveWindow("result_ov", 900, 350)
        #     cv2.imshow("result_ov", self.last_frame_OV_output)
        #
        # cv2.waitKey(0)

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
