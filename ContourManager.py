import numpy as np
import cv2
import math

# this class is going to contain all functions that manipulate contour-lists and are right now implemented in the Tracker-class
#


class ContourManager(object):

    def __init__(self, fish_size_threshold, fish_max_size_threshold):
        self._contour_list = []

    @property
    def contour_list(self):
        return self._contour_list

    @contour_list.setter
    def contour_list(self, cnt_list):
        self._contour_list = cnt_list

    # # set a threshold for area. all contours with smaller area get deleted
    def del_small_contours(self, fish_size_threshold):
        area_threshold = fish_size_threshold
        if self._contour_list is not None and len(self._contour_list) > 0:

            counter = 0
            while counter < len(self._contour_list):

                popped = False

                if cv2.contourArea(self._contour_list[counter]) < area_threshold:
                    self._contour_list.pop(counter)
                    popped = True
                if not popped:
                    counter += 1

    def del_oversized_contours(self, fish_max_size_threshold):
        area_threshold = fish_max_size_threshold
        if self._contour_list is not None and len(self._contour_list) > 0:

            counter = 0
            while counter < len(self._contour_list):

                popped = False

                if cv2.contourArea(self._contour_list[counter]) > area_threshold:
                    self._contour_list.pop(counter)
                    popped = True
                if not popped:
                    counter += 1

    # # only keep biggest-area object in contour list
    def keep_biggest_contours(self):
        if self._contour_list is None or len(self._contour_list) == 0:
            return

        biggest = cv2.contourArea(self._contour_list[0])

        counter = 1
        while counter < len(self._contour_list):
            next_size = cv2.contourArea(self._contour_list[counter])
            if next_size < biggest:
                self._contour_list.pop(counter)
            elif next_size > biggest:
                biggest = next_size
                self._contour_list.pop(counter-1)
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
    def keep_nearest_contour(self, last_pos, ellipse, roi):
        if last_pos is None:
            last_pos = (roi.y2 - roi.y1, int((roi.x2 - roi.x1) / 2))

        cnt_center = self.get_center(ellipse[0])
        biggest_dist = self.calculate_distance(cnt_center, last_pos)

        counter = 1
        while counter < len(self._contour_list):
            next_center = self.get_center(ellipse[counter])
            next_dist = self.calculate_distance(next_center, last_pos)
            if next_dist < biggest_dist:
                self._contour_list.pop(counter)
            elif next_dist > biggest_dist:
                biggest_dist = next_dist
                self._contour_list.pop(counter-1)
            else:
                counter += 1
