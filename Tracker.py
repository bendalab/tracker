import numpy as np
import cv2
import math
import sys
import copy
import os
import argparse

class Tracker():
    def __init__(self):
        # program data
        self.output_directory = ""
        self.dir = "examples/"
        self.videofile_name = "2014-08-27_33"
        # self.dir = "examples/"
        # self.videofile_name = "2014-10-01_33"
        self.video_file = ""

        self.cap = ""

        self.save_frames = False
        self.frame_waittime = 25

        self.frame_counter = 0

        self.roi_x1 = 15
        self.roi_x2 = 695
        self.roi_y1 = 80
        self.roi_y2 = 515

        # image morphing data
        self.erosion_iterations = 1
        self.dilation_iterations = 4

        # tracking data
        self.contour_list = None

        self.fish_size_threshold = 700

        self.fish_started = False
        self.starting_area_x_factor = 0.85
        self.starting_area_x2_factor = 1.00
        self.starting_area_y1_factor = 0.30
        self.starting_area_y2_factor = 0.70

        self.last_pos = None
        self.all_pos_roi = []
        self.all_pos_original = []

        self.last_ori = None
        self.start_ori = 270
        self.all_oris = []

        self.ellipse = None
        self.line = None
        self.line_point_offset = 5
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

        self.draw_contour = False
        self.draw_ellipse = True
        self.draw_line = True
        self.draw_travel_orientation = True
        self.draw_travel_route = True
        self.draw_original_output = True

        self.estimate_missing_data = True
        self.estimated_pos_roi = []
        self.estimated_pos_original = []
        self.estimated_oris = []

    @staticmethod
    def show_imgs(img, roi_output, roi_bg_sub, mo_roi_bg_sub, edges):
        return

    # sets video file to terminal-attribute path to video file
    def set_video_file(self):
        if len(sys.argv) > 1:
            self.video_file = sys.argv[1]
        else:
            self.video_file = self.dir + self.videofile_name + ".avi"
            return

    def check_if_necessary_files_exist(self):
        if not os.path.exists(self.video_file):
            sys.exit("ERROR: Video File does not exist - Tracking aborted")

    def extract_video_file_name_and_path(self):
        pointer_end = len(self.video_file)-1
        while self.video_file[pointer_end] != ".":
            pointer_end -= 1
            if pointer_end == 0:
                print "no valid file"
                return ""

        pointer_start = pointer_end
        while self.video_file[pointer_start-1] != "/":
            pointer_start -= 1

        return self.video_file[pointer_start:pointer_end], self.video_file[:pointer_start]

    # captures video defined by path stored in video file
    def set_video_capture(self):
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
            self.last_pos = (self.roi_y2-self.roi_y1, int((self.roi_x2-self.roi_x1)/2))

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
        non_starting_area_x = int(self.starting_area_x_factor * width)
        non_starting_area_y1 = int(self.starting_area_y1_factor * height)
        non_starting_area_y2 = int(self.starting_area_y2_factor * height)

        if self.contour_list is not None:
            for i in range(0, len(self.contour_list)):
                cnt = self.contour_list[i]
                ellipse = cv2.fitEllipse(cnt)
                if ellipse[0][0] > non_starting_area_x and ellipse[0][1] > non_starting_area_y1 and ellipse[0][1] < non_starting_area_y2:
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

        x1 = int(round(center_x - self.line_point_offset*x_dif))
        y1 = int(round(center_y - self.line_point_offset*y_dif))
        x2 = int(round(center_x + self.line_point_offset*x_dif))
        y2 = int(round(center_y + self.line_point_offset*y_dif))

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
            original_x = self.last_pos[0]+self.roi_x1
            original_y = self.last_pos[1]+self.roi_y1
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
                    self.estimated_pos_original[pointer] = (self.estimated_pos_roi[pointer][0] + self.roi_x1, self.estimated_pos_roi[pointer][1] + self.roi_y1)
                    first_pos_estimated = True
                else:
                    self.estimated_pos_roi[pointer] = ((self.estimated_pos_roi[pointer-1][0] + value_diff_x_part), (self.estimated_pos_roi[pointer-1][1] + value_diff_y_part))
                    self.estimated_pos_original[pointer] = (self.estimated_pos_roi[pointer][0] + self.roi_x1, self.estimated_pos_roi[pointer][1] + self.roi_y1)
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
                cv2.circle(self.last_frame, (int(round(c[0])), int(round(c[1]))), 2, (0, 0, 255))
                cv2.circle(self.last_frame_OV_output, (int(round(c[0]))+self.roi_x1, int(round(c[1])+self.roi_y1)), 2, (0, 0, 255))

    def run(self):
        # create BG subtractor
        bg_sub = cv2.BackgroundSubtractorMOG2()

        # main loop
        while self.cap.isOpened():


            ret, frame = self.cap.read()

            if frame is None:
                break

            self.frame_counter += 1

            # set region of interest ROI
            roi = copy.copy(frame[self.roi_y1:self.roi_y2, self.roi_x1:self.roi_x2])
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
                    cv2.circle(roi, point, 2, (255, 0, 0))

            if self.draw_original_output:
                for coordinates in self.img_travel_orientation:
                    cv2.line(frame_output, (coordinates[0]+self.roi_x1, coordinates[1]+self.roi_y1), (coordinates[2]+self.roi_x1, coordinates[3]+self.roi_y1), (150,150,0), 1)
                for point in self.all_pos_original:
                    if point is not None:
                        cv2.circle(frame_output, (int(round(point[0])), int(round(point[1]))), 2, (255, 0, 0))

            # show all imgs
            if self.draw_original_output:
                self.show_imgs(frame_output, roi_output, roi_bg_sub, mo_roi_bg_sub, edges)
            else:
                self.show_imgs(frame, roi_output, roi_bg_sub, mo_roi_bg_sub, edges)

            # show output img
            cv2.imshow("contours", roi)
            # if SAVE_FRAMES:
            #     cv2.imwrite(dir + "frames/" + str(frame_counter) + "_contours" + ".jpg", roi)

            self.last_frame = roi
            self.last_frame_OV_output = frame_output

            if cv2.waitKey(self.frame_waittime) & 0xFF == 27:
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


    @staticmethod
    def fill_spaces(file, string):
        for i in range(0, 20-len(string)):
            file.write(" ")

    @staticmethod
    def print_None_to_file(file):
        for i in range(0, 16):
            file.write(" ")
        file.write("None")

    def save_data_to_files(self):
        file_name, file_directory = self.extract_video_file_name_and_path()

        ###
        ### save data into txt file
        ###

        # define ouput directory name as file name
        self.output_directory = file_directory + file_name

        #check if times file in same folder as video file
        times_file_path = file_directory + file_name + "_times.dat"
        times_file = None
        if not os.path.exists(times_file_path):
            sys.exit("ERROR: times file missing - data saving abortet")
        else:
            times_file = open(times_file_path, 'r')

        # create directory name after video file
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        # else:
        #     print "directory exists"

        output_file_path = self.output_directory + "/" + file_name + ".txt"
        output_file = open(output_file_path, 'w')

        output_file.write("# Tracking parameters:\n")
        output_file.write("#     Region of Interest X-Axis         : [" + str(self.roi_x1) + "," + str(self.roi_x2) + "]\n")
        output_file.write("#     Region of Interest Y-Axis         : [" + str(self.roi_y1) + "," + str(self.roi_y2) + "]\n")
        output_file.write("#     Fish size threshold               : " + str(self.fish_size_threshold) + "\n")
        output_file.write("#     Start orientation                 : " + str(self.start_ori) + "\n")
        output_file.write("#     Fish starting area X-Axis factor  : " + str(self.starting_area_x_factor) + "\n")
        output_file.write("#     Fish starting area Y-Axis factor 1: " + str(self.starting_area_y1_factor) + "\n")
        output_file.write("#     Fish starting area Y-Axis factor 2: " + str(self.starting_area_y2_factor) + "\n")
        output_file.write("#\n")
        output_file.write("#     Orientation algorithm assumes that fish can not turn more than >> 90 << degrees from one frame to the next\n")

        output_file.write("\n#Key\n")
        output_file.write("#           frame_time               pos_roi_x               pos_roi_y           est_pos_roi_x           est_pos_roi_y          pos_original_x          pos_original_y      est_pos_original_x      est_pos_original_y            orientations        est_orientations           obj_per_frame       fishobj_per_frame\n")

        lc = 0
        spacing = 4
        for line in times_file:

            output_file.write("  ")
            line = line.strip()
            self.fill_spaces(output_file, line)
            output_file.write(line)
            output_file.write(" "*spacing)

            if lc >= self.frame_counter:
                return

            if self.all_pos_roi[lc] is None:
                self.print_None_to_file(output_file)
            else:
                rounded_x_pos_original = str(round(self.all_pos_roi[lc][0], 2))
                self.fill_spaces(output_file, rounded_x_pos_original)
                output_file.write(rounded_x_pos_original)
            output_file.write(" "*spacing)

            if self.all_pos_roi[lc] is None:
                self.print_None_to_file(output_file)
            else:
                rounded_y_pos_original = str(round(self.all_pos_roi[lc][1], 2))
                self.fill_spaces(output_file, rounded_y_pos_original)
                output_file.write(rounded_y_pos_original)
            output_file.write(" "*spacing)

            if self.estimated_pos_roi[lc] is None:
                self.print_None_to_file(output_file)
            else:
                rounded_est_x_pos_original = str(round(self.estimated_pos_roi[lc][0], 2))
                self.fill_spaces(output_file, rounded_est_x_pos_original)
                output_file.write(rounded_est_x_pos_original)
            output_file.write(" "*spacing)

            if self.estimated_pos_roi[lc] is None:
                self.print_None_to_file(output_file)
            else:
                rounded_est_y_pos_original = str(round(self.estimated_pos_roi[lc][1], 2))
                self.fill_spaces(output_file, rounded_est_y_pos_original)
                output_file.write(rounded_est_y_pos_original)
            output_file.write(" "*spacing)


            if self.all_pos_original[lc] is None:
                self.print_None_to_file(output_file)
            else:
                rounded_x_pos_original = str(round(self.all_pos_original[lc][0], 2))
                self.fill_spaces(output_file, rounded_x_pos_original)
                output_file.write(rounded_x_pos_original)
            output_file.write(" "*spacing)

            if self.all_pos_original[lc] is None:
                self.print_None_to_file(output_file)
            else:
                rounded_y_pos_original = str(round(self.all_pos_original[lc][1], 2))
                self.fill_spaces(output_file, rounded_y_pos_original)
                output_file.write(rounded_y_pos_original)
            output_file.write(" "*spacing)

            if self.estimated_pos_original[lc] is None:
                self.print_None_to_file(output_file)
            else:
                rounded_est_x_pos_original = str(round(self.estimated_pos_original[lc][0], 2))
                self.fill_spaces(output_file, rounded_est_x_pos_original)
                output_file.write(rounded_est_x_pos_original)
            output_file.write(" "*spacing)

            if self.estimated_pos_original[lc] is None:
                self.print_None_to_file(output_file)
            else:
                rounded_est_y_pos_original = str(round(self.estimated_pos_original[lc][1], 2))
                self.fill_spaces(output_file, rounded_est_y_pos_original)
                output_file.write(rounded_est_y_pos_original)
            output_file.write(" "*spacing)

            if self.all_oris[lc] is None:
                self.print_None_to_file(output_file)
            else:
                rounded_ori = str(round(self.all_oris[lc], 2))
                self.fill_spaces(output_file, rounded_ori)
                output_file.write(rounded_ori)
            output_file.write(" "*spacing)

            if self.estimated_oris[lc] is None:
                self.print_None_to_file(output_file)
            else:
                rounded_est_ori = str(round(self.estimated_oris[lc], 2))
                self.fill_spaces(output_file, rounded_est_ori)
                output_file.write(rounded_est_ori)
            output_file.write(" "*spacing)

            cnt_of_frame = str(self.number_contours_per_frame[lc])
            self.fill_spaces(output_file, cnt_of_frame)
            output_file.write(cnt_of_frame)
            output_file.write(" "*spacing)

            rel_cnt_of_frame = str(self.number_relevant_contours_per_frame[lc])
            self.fill_spaces(output_file, rel_cnt_of_frame)
            output_file.write(rel_cnt_of_frame)



            output_file.write("\n")

            lc += 1

        #save last frame
        cv2.imwrite(self.output_directory + "/" + file_name + "_OV_path.png", self.last_frame_OV_output)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tracking fish in video file')
    parser.add_argument('path', type=str, help="absolute file path to video including file name and file extension")
    args = parser.parse_args()


    cv2.namedWindow("contours")
    cv2.moveWindow("contours", 570, 570)

    tr = Tracker()

    tr.set_video_file()
    tr.check_if_necessary_files_exist()
    tr.set_video_capture()

    tr.run()

    tr.estimate_missing_pos()
    tr.estimate_missing_ori()
    tr.draw_estimated_data()

    # tr.print_data()
    tr.check_data_integrity()

    # cv2.namedWindow("result")
    # cv2.moveWindow("result", 200, 350)
    # cv2.imshow("result", tr.last_frame)

    # if SAVE_FRAMES:
    #     cv2.imwrite(dir + "frames/" + str(frame_counter) + "_estimation" + ".jpg", last_frame)

    tr.save_data_to_files()

    if tr.draw_original_output:
        cv2.namedWindow("result_ov")
        cv2.moveWindow("result_ov", 900, 350)
        cv2.imshow("result_ov", tr.last_frame_OV_output)

    cv2.waitKey(0)
