import cv2
import math

class ImageManager(object):

    def __init__(self):
        self._last_frame = None
        self._last_frame_ov_output = None

        self._img_travel_orientation = []
        self._img_travel_route = []

        self._lineend_offset = 5
        self._circle_size = 2

        self._draw_contour = False
        self._draw_ellipse = True
        self._draw_line = True
        self._lx1 = 0
        self._ly1 = 0
        self._lx2 = 0
        self._ly2 = 0
        self._draw_travel_orientation = True
        self._draw_travel_route = True
        self._draw_original_output = True
        self._show_bg_sub_img = False
        self._show_morphed_img = False

        # calculates start and endpoint for a line displaying the orientation of given ellipse (thus of the fish)
    def get_line_from_ellipse(self, ellipse):
        center_x = ellipse[0][0]
        center_y = ellipse[0][1]
        grade_angle = -1 * ellipse[2]
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

    def append_to_travel_route(self, ellipse):
        if ellipse is not None:
            ellipse_x = int(round(ellipse[0][0]))
            ellipse_y = int(round(ellipse[0][1]))
            point = (ellipse_x, ellipse_y)
            self.img_travel_route.append(point)

    def draw_extracted_data(self, ellipse, bool_fish_started, roi_img, contour_list):
        # draw data for visual feedback while tracking
        # draw ellipse
        if self._draw_ellipse and ellipse is not None and bool_fish_started:
            cv2.ellipse(roi_img, ellipse, (0, 0, 255), 2)

        # draw countours to ROI img and show img
        if self.draw_contour:
            cv2.drawContours(roi_img, contour_list, -1, (0, 255, 0), 3)

        # draw travel route
        if self.draw_travel_orientation:
            for coordinates in self.img_travel_orientation:
                cv2.line(roi_img, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), (150,150,0), 1)

        # draw travel orientation
        if self.draw_travel_route:
            for point in self.img_travel_route:
                cv2.circle(roi_img, point, self._circle_size, (255, 0, 0))

    def draw_data_on_overview_image(self, roi, dm):
        # draw data for output image
        if self.draw_original_output:
            for coordinates in self.img_travel_orientation:
                cv2.line(self.last_frame_ov_output, (coordinates[0] + roi.x1, coordinates[1] + roi.y1),
                         (coordinates[2] + roi.x1, coordinates[3] + roi.y1), (150,150,0), 1)
            for point in dm.all_pos_original:
                if point is not None:
                    cv2.circle(self.last_frame_ov_output, (int(round(point[0])), int(round(point[1]))), self._circle_size, (255, 0, 0))

    def draw_estimated_data(self, boo_estimate_missing_data, estimated_pos_roi, roi, circle_size):
        if not boo_estimate_missing_data:
            return

        for c in estimated_pos_roi:
            if c is not None:
                cv2.circle(self.last_frame, (int(round(c[0])), int(round(c[1]))), circle_size, (0, 0, 255))
                cv2.circle(self.last_frame_ov_output, (int(round(c[0])) + roi.x1, int(round(c[1]) + roi.y1)), circle_size, (0, 0, 255))





    @property
    def img_travel_orientation(self):
        return self._img_travel_orientation

    @property
    def img_travel_route(self):
        return self._img_travel_route

    @property
    def last_frame(self):
        return self._last_frame
    @last_frame.setter
    def last_frame(self, frame):
        self._last_frame = frame

    @property
    def last_frame_ov_output(self):
        return self._last_frame_ov_output
    @last_frame_ov_output.setter
    def last_frame_ov_output(self, frame):
        self._last_frame_ov_output = frame

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
    def draw_line(self):
        return self._draw_line
    @draw_line.setter
    def draw_line(self, boo):
        self._draw_line = boo

    @property
    def draw_travel_orientation(self):
        return self._draw_travel_orientation
    @draw_travel_orientation.setter
    def draw_travel_orientation(self, boo):
        self._draw_travel_orientation = boo

    @property
    def draw_travel_route(self):
        return self._draw_travel_route
    @draw_travel_route.setter
    def draw_travel_route(self, boo):
        self._draw_travel_route = boo

    @property
    def draw_original_output(self):
        return self._draw_original_output
    @draw_original_output.setter
    def draw_original_output(self, boo):
        self._draw_original_output = boo

    @property
    def show_bg_sub_img(self):
        return self._show_bg_sub_img
    @show_bg_sub_img.setter
    def show_bg_sub_img(self, boo):
        self._show_bg_sub_img = boo

    @property
    def show_morphed_img(self):
        return self._show_morphed_img
    @show_morphed_img.setter
    def show_morphed_img(self, boo):
        self._show_morphed_img = boo

    @property
    def lx1(self):
        return self._lx1
    @lx1.setter
    def lx1(self, value):
        self._lx1 = value

    @property
    def lx2(self):
        return self._lx2
    @lx2.setter
    def lx2(self, value):
        self._lx2 = value

    @property
    def ly1(self):
        return self._ly1
    @ly1.setter
    def ly1(self, value):
        self._ly1 = value

    @property
    def ly2(self):
        return self._ly2
    @ly2.setter
    def ly2(self, value):
        self._ly2 = value

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