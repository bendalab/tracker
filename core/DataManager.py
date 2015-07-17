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
        self._last_ori_ratio = None
        self._all_oris_ratio = []

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

    def set_last_orientation(self, cnt, image_manager):
        if cnt is not None and len(cnt) > 0:
            # put rectangle on contour
            self._fish_box = cv2.minAreaRect(cnt[0])
            f = self._fish_box
            self._fish_box = (f[0], f[1], f[2])
            # box[0] -> center
            # box[1] -> size
            # box[2] -> angle
            b = self._fish_box

            fac = 0.5

            if b[1][0] > b[1][1]:
                grade_angle = -1 * b[2]
                angle_prop = grade_angle/180
                angle = math.pi*angle_prop
                dx = int(round((b[1][0]/2)*math.cos(angle)))
                dy = -int(round((b[1][0]/2)*math.sin(angle)))

                center1 = tuple((map(operator.add, b[0], (int(dx*fac), int(dy*fac)))))
                self._back_box = (center1, (int(b[1][0]*fac), int(b[1][1])), b[2])
                center2 = tuple((map(operator.sub, b[0], (int(dx*fac), int(dy*fac)))))
                self._front_box = (center2, (int(b[1][0]*fac), int(b[1][1])), b[2])

            else:
                grade_angle = -1 * b[2]
                angle_prop = grade_angle/180
                angle = math.pi*angle_prop
                dx = int(round((b[1][1]/2)*math.sin(angle)))
                dy = int(round((b[1][1]/2)*math.cos(angle)))

                center1 = tuple((map(operator.add, b[0], (int(dx*fac), int(dy*fac)))))
                self._back_box = (center1, (int(b[1][0]), int(b[1][1]*fac)), b[2])
                center2 = tuple((map(operator.sub, b[0], (int(dx*fac), int(dy*fac)))))
                self._front_box = (center2, (int(b[1][0]), int(b[1][1]*fac)), b[2])

            # get points of rectangle
            self.fish_box_points = cv2.cv.BoxPoints(self.fish_box)
            self.fish_box_points = np.int0(self.fish_box_points)
            self.front_box_points = cv2.cv.BoxPoints(self._front_box)
            self.front_box_points = np.int0(self.front_box_points)
            self.back_box_points = cv2.cv.BoxPoints(self._back_box)
            self.back_box_points = np.int0(self.back_box_points)

            # check where front and back is
            # counters for white pixels
            front_counter = 0
            back_counter = 0

            y_list, x_list = np.nonzero(image_manager.current_bg_sub)

            for i in range(len(x_list)):
                point = (x_list[i], y_list[i])
                # print point
                if cv2.pointPolygonTest(self.front_box_points, point, False) > 0:
                    front_counter += 1
                if cv2.pointPolygonTest(self.back_box_points, point, False) > 0:
                    back_counter += 1

            if back_counter > front_counter:
                self.front_box_points, self.back_box_points = self.back_box_points, self.front_box_points
                back_counter, front_counter = front_counter, back_counter

            front_center = np.mean(self.front_box_points, 0).astype(int)
            back_center = np.mean(self.back_box_points, 0).astype(int)

            dx = front_center[0] - back_center[0]
            dy = -1*(front_center[1] - back_center[1])

            pi_angle = math.atan2(dx, dy)
            if pi_angle < 0:
                pi_angle += math.pi*2

            rel = pi_angle/(2*math.pi)
            self._last_ori = rel*360
            self._last_ori_ratio = float(front_counter)/back_counter

    def save_fish_orientations(self, ellipse, bool_fish_started):
        if not bool_fish_started or ellipse is None:
            self._all_oris.append(None)
            self._all_oris_ratio.append(None)
            return

        self._all_oris.append(self._last_ori)
        self._all_oris_ratio.append(self._last_ori_ratio)

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
    def all_oris_ratio(self):
        return self._all_oris_ratio

    @property
    def front_box(self):
        return self._front_box

    @property
    def back_box(self):
        return self._back_box

    @property
    def fish_box(self):
        return self._fish_box