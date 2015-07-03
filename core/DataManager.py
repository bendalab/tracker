import numpy as np
import operator
import math
import cv2

class DataManager(object):

    def __init__(self):
        self._frame_counter = 0

        self._video_resolution = None

        self._last_pos = None
        self._all_pos_roi = []
        self._all_pos_original = []

        self._last_ori = None
        self._all_oris = []

        self._fish_not_detected_count = 0

        self._number_contours_per_frame = []
        self._number_relevant_contours_per_frame = []

        self._estimated_pos_roi = []
        self._estimated_pos_original = []
        self._estimated_oris = []

        self._fish_box = None
        self.fish_box_points = None
        self._front_box = None
        self._back_box = None
        self.front_box_points = None
        self.back_box_points = None

    @staticmethod
    def save_number_of_contours(cnt_list, number_cnt_list):
        if cnt_list is None:
            number_cnt_list.append(0)
        else:
            number_cnt_list.append(len(cnt_list))

    # def set_last_pos(self, ellipse):
    #     if ellipse is None:
    #         self.last_pos = None
    #         return
    #     else:
    #         self.last_pos = ellipse[0]

    def set_last_pos(self, clist):
        if clist is None or len(clist) == 0:
            self.last_pos = None
        else:
            self.last_pos = np.mean(clist[0], 0)[0]

    def save_fish_positions(self, roi):
        self.all_pos_roi.append(self.last_pos)
        if self.last_pos is None:
            self.all_pos_original.append(self.last_pos)
        else:
            original_x = self.last_pos[0] + roi.x1
            original_y = self.last_pos[1] + roi.y1
            self.all_pos_original.append((original_x, original_y))

    def calc_ori_boxes(self, cnt, tracking_area):
        if cnt is not None and len(cnt) > 0:
            # put rectangle on contour
            self._fish_box = cv2.minAreaRect(cnt[0])
            f = self._fish_box
            self._fish_box = (f[0], f[1], f[2])
            # box[0] -> center
            # box[1] -> size
            # box[2] -> angle
            b = self._fish_box

            if b[1][0] > b[1][1]:
                grade_angle = -1 * b[2]
                angle_prop = grade_angle/180
                angle = math.pi*angle_prop
                dx = int(round((b[1][0]/2)*math.cos(angle)))
                dy = -int(round((b[1][0]/2)*math.sin(angle)))

                fac = 2
                center1 = tuple((map(operator.add, b[0], (int(dx*fac), int(dy*fac)))))
                self._front_box = (center1, (int(b[1][0]), b[1][1]), b[2])
                center2 = tuple((map(operator.sub, b[0], (int(dx*fac), int(dy*fac)))))
                self._back_box = (center2, (int(b[1][0]), b[1][1]), b[2])

            else:
                grade_angle = -1 * b[2]
                angle_prop = grade_angle/180
                angle = math.pi*angle_prop
                dx = int(round((b[1][1]/2)*math.sin(angle)))
                dy = int(round((b[1][1]/2)*math.cos(angle)))

                center1 = tuple((map(operator.add, b[0], (int(dx*2), int(dy*2)))))
                self._front_box = (center1, (int(b[1][0]), b[1][1]), b[2])
                center2 = tuple((map(operator.sub, b[0], (int(dx*2), int(dy*2)))))
                self._back_box = (center2, (int(b[1][0]), b[1][1]), b[2])



            # offset = [tracking_area.x1, tracking_area.y1]
            # fish_box_list = list(self._fish_box)
            # fish_box_list[0] = tuple(map(operator.add, fish_box_list[0], offset))
            # self._fish_box = tuple(fish_box_list)

            # get points of rectangle
            self.fish_box_points = cv2.cv.BoxPoints(self.fish_box)
            self.fish_box_points = np.int0(self.fish_box_points)
            self.front_box_points = cv2.cv.BoxPoints(self._front_box)
            self.front_box_points = np.int0(self.front_box_points)
            self.back_box_points = cv2.cv.BoxPoints(self._back_box)
            self.back_box_points = np.int0(self.back_box_points)



    def set_last_orientation(self, ellipse, bool_fish_started, start_ori):
        if not bool_fish_started or ellipse is None:
            return

        if self.last_ori is None:
            self.last_ori = start_ori

        if ellipse is None:
            return

        ell_ori = ellipse[2]
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

    def save_fish_orientations(self, ellipse, bool_fish_started):
        if not bool_fish_started:
            self.all_oris.append(None)
            return

        if ellipse is None:
            self.all_oris.append(None)
            return

        self.all_oris.append(self.last_ori)

    def estimate_missing_pos(self, roi):
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
                    self.estimated_pos_original[pointer] = (self.estimated_pos_roi[pointer][0] + roi.x1, self.estimated_pos_roi[pointer][1] + roi.y1)
                    first_pos_estimated = True
                else:
                    self.estimated_pos_roi[pointer] = ((self.estimated_pos_roi[pointer-1][0] + value_diff_x_part), (self.estimated_pos_roi[pointer-1][1] + value_diff_y_part))
                    self.estimated_pos_original[pointer] = (self.estimated_pos_roi[pointer][0] + roi.x1, self.estimated_pos_roi[pointer][1] + roi.y1)
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

    def copy_original_to_est_data(self):
        for i in range(0, self.frame_counter):
            if self.all_pos_roi[i] is not None:
                self.estimated_pos_roi[i] = self.all_pos_roi[i]
            if self.all_pos_original[i] is not None:
                self.estimated_pos_original[i] = self.all_pos_original[i]
            if self.all_oris[i] is not None:
                self.estimated_oris[i] = self.all_oris[i]

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

    def check_frames_missing_fish(self, fish_not_detected_threshold):
        start_pos = 0
        for entry in self.all_oris:
            if entry is None:
                start_pos += 1

        for i in range(start_pos, len(self.all_oris), 1):
            if self.all_oris[i] is None:
                self.fish_not_detected_count += 1

        if self.fish_not_detected_count > fish_not_detected_threshold:
            self.fish_not_detected_threshold_reached = True

    @property
    def frame_counter(self):
        return self._frame_counter
    @frame_counter.setter
    def frame_counter(self, value):
        self._frame_counter = value

    @property
    def video_resolution(self):
        return self._video_resolution
    @video_resolution.setter
    def video_resolution(self, tuple):
        self._video_resolution = tuple

    @property
    def last_pos(self):
        return self._last_pos
    @last_pos.setter
    def last_pos(self, value):
        self._last_pos = value

    @property
    def all_pos_roi(self):
        return self._all_pos_roi

    @property
    def all_pos_original(self):
        return self._all_pos_original

    @property
    def last_ori(self):
        return self._last_ori
    @last_ori.setter
    def last_ori(self, value):
        self._last_ori = value

    @property
    def all_oris(self):
        return self._all_oris

    @property
    def fish_not_detected_count(self):
        return self._fish_not_detected_count
    @fish_not_detected_count.setter
    def fish_not_detected_count(self, value):
        self._fish_not_detected_count = value

    @property
    def number_contours_per_frame(self):
        return self._number_contours_per_frame

    @property
    def number_relevant_contours_per_frame(self):
        return self._number_relevant_contours_per_frame

    @property
    def estimated_pos_roi(self):
        return self._estimated_pos_roi

    @property
    def estimated_pos_original(self):
        return self._estimated_pos_original

    @property
    def estimated_oris(self):
        return self._estimated_oris

    @property
    def front_box(self):
        return self._front_box

    @property
    def back_box(self):
        return self._back_box

    @property
    def fish_box(self):
        return self._fish_box