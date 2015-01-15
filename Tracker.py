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
import collections


class Tracker(object):
    def __init__(self, path=None, nix_io=False):
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
        
        self.cap = ""

        self.save_frames = False
        self.frame_waittime = 50

        self.frame_counter = 0

        # self.__roi = ROI(15, 695, 80, 515) # Eileen setup
        self.__roi = ROI(160, 80, 700, 525) # Isabell setup

        # image morphing data
        self.erosion_iterations = 1
        self.dilation_iterations = 4

        # tracking data
        self.contour_list = None

        # fish size thresholds
        self.fish_size_threshold = 700
        self.fish_max_size_threshold = 4000
        self.enable_max_size_threshold = False

        self.fish_started = False
        self.starting_area_x1_factor = 0.85
        self.starting_area_x2_factor = 1.00
        self.starting_area_y1_factor = 0.30
        self.starting_area_y2_factor = 0.70

        self.last_pos = None
        self.all_pos_roi = []
        self.all_pos_original = []

        self.last_ori = None
        self.start_ori = 270
        self.all_oris = []

        self.fish_not_detected_count = 0
        self.fish_not_detected_threshold = 50
        self.fish_not_detected_threshold_reached = False

        self.ellipse = None
        self.line = None
        self.lineend_offset = 5
        self.circle_size = 2
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
        self.draw_contour = False
        self.draw_ellipse = True
        self.draw_line = True
        self.draw_travel_orientation = True
        self.draw_travel_route = True
        self.draw_original_output = True
        self.show_bg_sub_img = False
        self.show_morphed_img = False

        self.estimate_missing_data = True
        self.estimated_pos_roi = []
        self.estimated_pos_original = []
        self.estimated_oris = []

        # TODO import config file values
        self.will_import_config_values = True
        if self.will_import_config_values:
            self.import_config_values()

    @property
    def roi(self):
        return self.__roi

    def import_config_values(self):
        if not self.will_import_config_values:
            return
        if not os.path.exists('tracker.cnf'):
            print "Couldn't import config data from file - file doesn't exist"
            return

        cfg = ConfigParser.ConfigParser()
        cfg_file = open('tracker.cnf')
        cfg.readfp(cfg_file)

        self.erosion_iterations = cfg.getint('image_morphing', 'erosion_factor')
        self.dilation_iterations = cfg.getint('image_morphing', 'dilation_factor')
        # roi
        self.__roi.x1 = cfg.getint('roi', 'x1')
        self.__roi.x2 = cfg.getint('roi', 'x2')
        self.__roi.y1 = cfg.getint('roi', 'y1')
        self.__roi.y2 = cfg.getint('roi', 'y2')

        self.start_ori = cfg.getint('detection_values', 'start_orientation')
        self.fish_size_threshold = cfg.getint('detection_values', 'min_area_threshold')
        self.fish_max_size_threshold = cfg.getint('detection_values', 'max_area_threshold')
        self.enable_max_size_threshold = cfg.getboolean('detection_values', 'enable_max_size_threshold')

        self.frame_waittime = cfg.getint('system', 'frame_waittime')

        self.erosion_iterations = cfg.getint('image_morphing', 'erosion_factor')
        self.dilation_iterations = cfg.getint('image_morphing', 'dilation_factor')

        self.show_bg_sub_img = cfg.getboolean('image_processing', 'show_bg_sub_img')
        self.show_morphed_img = cfg.getboolean('image_processing', 'show_morphed_img')
        self.draw_contour = cfg.getboolean('image_processing', 'draw_contour')
        self.draw_ellipse = cfg.getboolean('image_processing', 'draw_ellipse')

        self.lineend_offset = cfg.getint('visualization', 'lineend_offset')
        self.circle_size = cfg.getint('visualization', 'circle_size')
        return

    # @staticmethod
    def show_imgs(self, img, roi_output, roi_bg_sub, mo_roi_bg_sub, edges):
        if self.show_bg_sub_img:
            cv2.imshow("bgsub", roi_bg_sub)
        if self.show_morphed_img:
            cv2.imshow("morphed_bgsub", mo_roi_bg_sub)
        return

    # sets video file to terminal-attribute path to video file
    def set_video_file(self):
        if len(sys.argv) > 1:
            self.video_file = sys.argv[1]
        else:
            return

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

    # captures video defined by path stored in video file
    def set_video_capture(self):
        print self.video_file
        self.cap = cv2.VideoCapture(self.video_file)

    # # morph given img by erosion/dilation
    def morph_img(self, img):
        # erode img
        er_kernel = np.ones((4, 4), np.uint8)
        er_img = cv2.erode(img, er_kernel, iterations=self.erosion_iterations)
        # dilate img
        di_kernel = np.ones((4, 4), np.uint8)
        di_img = cv2.dilate(er_img, di_kernel, iterations=self.dilation_iterations)
        # thresholding to black-white
        ret, morphed_img = cv2.threshold(di_img, 127, 255, cv2.THRESH_BINARY)
        # ret, morphed_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        return ret, morphed_img

    # # set a threshold for area. all contours with smaller area get deleted
    def del_small_contours(self):
        area_threshold = self.fish_size_threshold
        if self.contour_list is not None and len(self.contour_list) > 0:

            counter = 0
            while counter < len(self.contour_list):

                popped = False

                if cv2.contourArea(self.contour_list[counter]) < area_threshold:
                    self.contour_list.pop(counter)
                    popped = True
                if not popped:
                    counter += 1

    def del_oversized_contours(self):
        area_threshold = self.fish_max_size_threshold
        if self.contour_list is not None and len(self.contour_list) > 0:

            counter = 0
            while counter < len(self.contour_list):

                popped = False

                if cv2.contourArea(self.contour_list[counter]) > area_threshold:
                    self.contour_list.pop(counter)
                    popped = True
                if not popped:
                    counter += 1

    # # only keep biggest-area object in contour list
    def keep_biggest_contours(self):
        if self.contour_list is None or len(self.contour_list) == 0:
            return

        biggest = cv2.contourArea(self.contour_list[0])

        counter = 1
        while counter < len(self.contour_list):
            next_size = cv2.contourArea(self.contour_list[counter])
            if next_size < biggest:
                self.contour_list.pop(counter)
            elif next_size > biggest:
                biggest = next_size
                self.contour_list.pop(counter-1)
            else:
                counter += 1

    # calculates distance of two given points (tuples)
    @staticmethod
    def calculate_distance(p1, p2):
        x_diff = p2[0] - p1[0]
        y_diff = p2[1] - p1[1]
        dist = math.sqrt(x_diff*x_diff + y_diff*y_diff)
        return dist

    # get center of contour based on fitting ellipse
    @staticmethod
    def get_center(cnt):
        ellipse = cv2.fitEllipse(cnt)
        return ellipse[0]

    # if two or more contours (of same size) in contour_list delete which is farthest away from last pos fish was
    def keep_nearest_contour(self):
        if self.last_pos is None:
            self.last_pos = (self.roi.y2 - self.roi.y1, int((self.roi.x2 - self.roi.x1) / 2))

        cnt_center = self.get_center(self.ellipse[0])
        biggest_dist = self.calculate_distance(cnt_center, self.last_pos)

        counter = 1
        while counter < len(self.contour_list):
            next_center = self.get_center(self.ellipse[counter])
            next_dist = self.calculate_distance(next_center, self.last_pos)
            if next_dist < biggest_dist:
                self.contour_list.pop(counter)
            elif next_dist > biggest_dist:
                biggest_dist = next_dist
                self.contour_list.pop(counter-1)
            else:
                counter += 1

    @staticmethod
    def save_number_of_contours(cnt_list, number_cnt_list):
        if cnt_list is None:
            number_cnt_list.append(0)
        else:
            number_cnt_list.append(len(cnt_list))

    # check if fish started from the right side
    def check_if_fish_started(self, roi):
        height, width, depth = roi.shape
        non_starting_area_x1 = int(self.starting_area_x1_factor * width)
        non_starting_area_x2 = int(self.starting_area_x2_factor * width)
        non_starting_area_y1 = int(self.starting_area_y1_factor * height)
        non_starting_area_y2 = int(self.starting_area_y2_factor * height)

        if self.contour_list is not None:
            for i in range(0, len(self.contour_list)):
                cnt = self.contour_list[i]
                ellipse = cv2.fitEllipse(cnt)
                if ellipse[0][0] > non_starting_area_x1 and ellipse[0][0] < non_starting_area_x2 and ellipse[0][1] > non_starting_area_y1 and ellipse[0][1] < non_starting_area_y2:
                    self.fish_started = True

    # fitting ellipse onto contour
    def fit_ellipse_on_contour(self):
        if self.contour_list is None or len(self.contour_list) == 0:
            self.ellipse = None
        elif self.contour_list is not None and len(self.contour_list) > 0:
            if len(self.contour_list) > 0:
                cnt = self.contour_list[0]
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

        x1 = int(round(center_x - self.lineend_offset*x_dif))
        y1 = int(round(center_y - self.lineend_offset*y_dif))
        x2 = int(round(center_x + self.lineend_offset*x_dif))
        y2 = int(round(center_y + self.lineend_offset*y_dif))

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
            self.last_ori = self.start_ori

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
                cv2.circle(self.last_frame, (int(round(c[0])), int(round(c[1]))), self.circle_size, (0, 0, 255))
                cv2.circle(self.last_frame_OV_output, (int(round(c[0])) + self.roi.x1, int(round(c[1]) + self.roi.y1)), self.circle_size, (0, 0, 255))

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
            ret,thresh_img = cv2.threshold(mo_roi_bg_sub, 127, 255, cv2.THRESH_BINARY)
            self.contour_list, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            # TODO
            # merge biggest contour with nearest
            # contour_list = merge_biggest_contour_with_nearest(contour_list)

            # save amount of contours
            self.save_number_of_contours(self.contour_list, self.number_contours_per_frame)

            # everything below fish_size_threshold is being ignored
            self.del_small_contours()

            # everything above fish_size_max_threshold is being ignored
            if self.enable_max_size_threshold:
                self.del_oversized_contours()

            # save number of remaining contours
            self.save_number_of_contours(self.contour_list, self.number_relevant_contours_per_frame)

            # check if fish started
            if not self.fish_started:
                self.check_if_fish_started(roi)

            # if fish hasn't started yet, delete all contours
            if not self.fish_started:
                self.contour_list = []

            # keep only biggest contours
            self.keep_biggest_contours()

            # if two or more contours (of same size) in list delete which is farthest away from last point
            if self.fish_started and self.contour_list is not None and len(self.contour_list) > 1:
                self.keep_nearest_contour()

            # draw countours to ROI img and show img
            if self.draw_contour:
                cv2.drawContours(roi, self.contour_list, -1, (0, 255, 0), 3)

            # fit ellipse on contour
            self.fit_ellipse_on_contour()
            # draw ellipse
            if self.draw_ellipse and self.ellipse is not None and self.fish_started:
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
                    cv2.circle(roi, point, self.circle_size, (255, 0, 0))

            if self.draw_original_output:
                for coordinates in self.img_travel_orientation:
                    cv2.line(frame_output, (coordinates[0] + self.roi.x1, coordinates[1] + self.roi.y1), 
                             (coordinates[2] + self.roi.x1, coordinates[3] + self.roi.y1), (150,150,0), 1)
                for point in self.all_pos_original:
                    if point is not None:
                        cv2.circle(frame_output, (int(round(point[0])), int(round(point[1]))), self.circle_size, (255, 0, 0))

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

        # cv2.namedWindow("contours")
        # cv2.moveWindow("contours", 50, 50)

        self.extract_data()
        self.estimate_missing_pos()
        self.estimate_missing_ori()
        self.draw_estimated_data()

        # self.print_data()
        self.check_frames_missing_fish()

        # cv2.namedWindow("result")
        # cv2.moveWindow("result", 200, 350)
        # cv2.imshow("result", self.last_frame)

        # if SAVE_FRAMES:
        #     cv2.imwrite(dir + "frames/" + str(frame_counter) + "_estimation" + ".jpg", last_frame)

        file_name, file_directory = self.extract_video_file_name_and_path()
        if file_name == "":
            print "d1"
            return

        times = self.load_frame_times(file_directory + file_name + "_times.dat")
        output_file_name = file_directory + file_name + "/" + file_name
        params = {}
        params['fish size'] = self.fish_size_threshold
        params['start ori'] = self.start_ori
        params['starting area x1'] = self.starting_area_x1_factor
        params['starting area x2'] = self.starting_area_x2_factor
        params['starting area y1'] = self.starting_area_y1_factor
        params['starting area y2'] = self.starting_area_y2_factor
        params['source file'] = self.video_file
        if not self.nix_io:
            DataWriter.write_ascii(output_file_name + ".txt", times, self.all_pos_original, self.all_oris,
                                   self.estimated_pos_original, self.estimated_oris, self.number_contours_per_frame, 
                                   self.number_relevant_contours_per_frame, self.roi, self.frame_counter, params)
        else:
            DataWriter.write_nix(output_file_name + ".h5", times, self.all_pos_original, self.all_oris, 
                                 self.estimated_pos_original, self.estimated_oris, self.number_contours_per_frame, 
                                 self.number_relevant_contours_per_frame, self.roi, params)
        cv2.imwrite(file_directory + file_name + "/" + file_name + "_OV_path.png", self.last_frame_OV_output)

        self.check_data_integrity()

        # if self.draw_original_output:
        #     cv2.namedWindow("result_ov")
        #     cv2.moveWindow("result_ov", 900, 350)
        #     cv2.imshow("result_ov", self.last_frame_OV_output)
        #
        # cv2.waitKey(0)

class ROI(object):
    def __init__(self, x_1, y_1, x_2, y_2):
        self.__x_1 = x_1
        self.__y_1 = y_1
        self.__x_2 = x_2
        self.__y_2 = y_2

    @property
    def x1(self):
        return self.__x_1
    
    @x1.setter
    def x1(self, x):
        self.__x_1 = x

    @property
    def y1(self):
        return self.__y_1

    @y1.setter
    def y1(self, x):
        self.__y_1 = x
    
    @property
    def x2(self):
        return self.__x_2

    @x2.setter
    def x2(self, x):
        self.__x_2 = x
    
    @property
    def y2(self):
        return self.__y_2

    @y2.setter
    def y2(self, x):
        self.__y_2 = x


class DataWriter(object):

    @staticmethod
    def fill_spaces(file, string):
        file.write(" " * (20 - len(string)))

    @staticmethod
    def print_none_to_file(file):
        file.write(" " * 16)
        file.write("None")

    @staticmethod
    def write_position(p, out_file, spacing):
        if p is None:
            DataWriter.print_none_to_file(out_file)
            out_file.write(" " * spacing)
        else:
            p = str(round(p, 2))
            DataWriter.fill_spaces(out_file, p)
            out_file.write(p)
            out_file.write(" " * spacing)

    @staticmethod
    def write_ascii(file_name, times, position, orientation, est_position, est_orientation, object_count, fish_object_count, roi, frame_count, parameters):
        """
         save data to text file
        """
        spacing = 4
        out_dir = '/'.join(file_name.split('/')[:-1])
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        none_count = 0
        for p in position:
            if p is None:
                none_count += 1

        output_file = open(file_name, 'w')
        output_file.write("# Tracking parameters:\n")
        output_file.write("#     Region of Interest X-Axis         : [" + str(roi.x1) + "," + str(roi.x2) + "]\n")
        output_file.write("#     Region of Interest Y-Axis         : [" + str(roi.y1) + "," + str(roi.y2) + "]\n")
        output_file.write("#     Fish size threshold               : " + str(parameters['fish size']) + "\n")
        output_file.write("#     Start orientation                 : " + str(parameters['start ori']) + "\n")
        output_file.write("#     Fish starting area X-Axis factor1 : " + str(parameters['starting area x1']) + "\n")
        output_file.write("#     Fish starting area X-Axis factor2 : " + str(parameters['starting area x2']) + "\n")
        output_file.write("#     Fish starting area Y-Axis factor1 : " + str(parameters['starting area y1']) + "\n")
        output_file.write("#     Fish starting area Y-Axis factor2 : " + str(parameters['starting area y2']) + "\n")
        output_file.write("#\n")
        output_file.write("#     Orientation algorithm assumes that fish can not turn more than >> 90 << degrees from one frame to the next\n")
        if none_count > 0:
            output_file.write("#\n")
            output_file.write("#     WARNING: Fish was not detected in " + str(none_count) + " of " + str(len(times)) + " frames. Orientation data may be incorrect.\n")

        output_file.write("\n#Key\n")
        output_file.write("#           frame_time               pos_roi_x               pos_roi_y           est_pos_roi_x           est_pos_roi_y          pos_original_x          pos_original_y      est_pos_original_x      est_pos_original_y            orientations        est_orientations           obj_per_frame       fishobj_per_frame\n")

        for i, t in enumerate(times):
            output_file.write("  ")
            DataWriter.fill_spaces(output_file, t)
            output_file.write(t)
            output_file.write(" " * spacing)

            if i >= frame_count:
                return
            DataWriter.write_position(position[i][0] - roi.x1 if position[i] is not None else None, output_file, spacing) # x position roi
            DataWriter.write_position(position[i][1] - roi.y1 if position[i] is not None else None, output_file, spacing) # y position roi
            DataWriter.write_position(est_position[i][0] - roi.x1 if est_position[i] is not None else None, output_file, spacing) # estimated x position roi
            DataWriter.write_position(est_position[i][1] - roi.y1 if est_position[i] is not None else None, output_file, spacing) # estimated y position roi
            
            DataWriter.write_position(position[i][0] if position[i] is not None else None, output_file, spacing) # x position
            DataWriter.write_position(position[i][1] if position[i] is not None else None, output_file, spacing) # y position
            DataWriter.write_position(est_position[i][0] if est_position[i] is not None else None, output_file, spacing) # estimated x position
            DataWriter.write_position(est_position[i][1] if est_position[i] is not None else None, output_file, spacing) # estimated y position

            DataWriter.write_position(orientation[i], output_file, spacing) # orientation
            DataWriter.write_position(est_orientation[i], output_file, spacing) # estimated orientation
            

            cnt_of_frame = str(object_count[i])
            DataWriter.fill_spaces(output_file, cnt_of_frame)
            output_file.write(cnt_of_frame)
            output_file.write(" " * spacing)

            rel_cnt_of_frame = str(fish_object_count[i])
            DataWriter.fill_spaces(output_file, rel_cnt_of_frame)
            output_file.write(rel_cnt_of_frame)

            output_file.write("\n")
        output_file.close()

    @staticmethod
    def time_to_seconds(time):
        if isinstance(time, collections.Iterable) and not isinstance(time, str):
            return map(DataWriter.time_to_seconds, time)
        else:
            ts = time.split(':')
            seconds = 0.
            seconds += float(ts[0]) * 3600
            seconds += float(ts[1]) * 60
            seconds += float(ts[-1])
        return seconds

    @staticmethod
    def save_trace(time, data, nix_block, name, nix_type, label, unit=None):
        # get only those that are valid
        valid = []
        stamps = []
        for t, d in zip(time, data):
            if d is not None:
                valid.append(d)
                stamps.append(t)
        # check if valid data is tuple
        if len(valid) > 0 and isinstance(valid[0], tuple):
            d = np.zeros((len(valid), len(valid[0])))
            for i, v in enumerate(valid):
                d[i,:] = list(v)
            array = nix_block.create_data_array(name, nix_type, data=d)
            array.label = label
            if unit is not None:
                array.unit = unit
            dim = array.append_range_dimension(stamps)
            dim.label = 'time'
            dim.unit = 's'
            dim = array.append_set_dimension()
            dim.labels = ['x', 'y']
            return array
        else:
            d = np.asarray(valid)
            array = nix_block.create_data_array(name, nix_type, data=d)
            array.label = label
            if unit is not None:
                array.unit = unit
            dim = array.append_range_dimension(stamps)
            dim.label = 'time'
            dim.unit = 's'
            return array

    @staticmethod
    def write_nix(file_name, times, position, orientation, est_position, est_orientation, object_count, fish_object_count, roi, parameters):
        import nix
        name = file_name.split('/')[-1].split('.')[0]
        nix_file = nix.File.open(file_name, nix.FileMode.Overwrite)
        block = nix_file.create_block(name, 'nix.tracking')

        # some metadata
        recording = nix_file.create_section('recording', 'recording')
        recording['Date'] = name.split('_')[0]
        recording['Experimenter'] = 'Some One'

        tracker = nix_file.create_section('Tracker', 'software.tracker')
        tracker['Version'] = 0.5
        tracker['Source location'] = 'raven.am28.uni-tuebingen.de:tracker.git'
        settings = tracker.create_section('settings', 'software.settings')
        settings['Region of Interest X'] = roi.x1
        settings['Region of Interest Y'] = roi.y1
        settings['Region of Interest width'] = roi.x2 - roi.x1
        settings['Region of Interest height'] = roi.y2 - roi.y1
        settings['Fish size threshold'] = parameters['fish size']
        settings['Start orientation'] = parameters['start ori']
        settings['Fish starting area X-Axis factor1'] = parameters['starting area x1']
        settings['Fish starting area X-Axis factor2'] = parameters['starting area x2']
        settings['Fish starting area Y-Axis factor1'] = parameters['starting area y1']
        settings['Fish starting area Y-Axis factor2'] = parameters['starting area y2']

        movie = nix_file.create_section('Movie', 'recording.movie')
        movie['Filename'] = parameters['source file']

        camera = movie.create_section('Camera', 'hardware.camera')
        camera['Model'] = 'Guppy F-038B NIR'
        camera['Vendor'] = 'Allied Vision Technologies'
        
        # create sources and link entities to metadata
        block.metadata = recording
        movie_source = block.create_source('Original movie', 'nix.source.movie')
        movie_source.metadata = movie
        tracking_source = block.create_source('Video tracking', 'nix.source.analysis')
        tracking_source.metadata = tracker

        # save data
        time_stamps = np.asarray(DataWriter.time_to_seconds(times))
        
        a = DataWriter.save_trace(time_stamps, position, block, 'positions', 'nix.irregular_sampled.coordinates', label='position')
        a.sources.append(movie_source)
        a.sources.append(tracking_source)
        
        a = DataWriter.save_trace(time_stamps, est_position, block, 'estimated positions', 'nix.irregular_sampled.coordinates', label='position')
        a.sources.append(movie_source)
        a.sources.append(tracking_source)

        a = DataWriter.save_trace(time_stamps, orientation, block, 'orientations', 'nix.irregular_sampled', label='orientation')
        a.sources.append(movie_source)
        a.sources.append(tracking_source)

        a = DataWriter.save_trace(time_stamps, est_orientation, block, 'estimated_orientations', 'nix.irregular_sampled', label='orientation')
        a.sources.append(movie_source)
        a.sources.append(tracking_source)
        
        a = DataWriter.save_trace(time_stamps, object_count, block, 'object count', 'nix.irregular_sampled', label='count')
        a.sources.append(movie_source)
        a.sources.append(tracking_source)
        
        a = DataWriter.save_trace(time_stamps, fish_object_count, block, 'fish object count', 'nix.irregular_sampled', label='count')
        a.sources.append(movie_source)
        a.sources.append(tracking_source)

        # TODO need more metadata like info about the subject, who, when, where etc. 
        # TODO If we support this (and we should suupport this) in the gui, we probably need a more elaborate DataWriter class!
        nix_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tracking fish in video file')
    parser.add_argument('path', type=str, help="absolute file path to video including file name and file extension")
    parser.add_argument('-n', '--nix_output', type=bool, default=False,
                        help="output tracking results to nix file")

    args = parser.parse_args()
    if not os.path.exists(args.path):
        print('File does not exist!')
        exit()
    tr = Tracker(args.path, args.nix_output)
    tr.run()
