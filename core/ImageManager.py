import cv2
import math
from copy import copy


class ImageManager(object):

    def __init__(self):
        self._current_frame = None
        self._current_bg_sub = None
        self._current_morphed = None
        self._overview_output = None

        self._lineend_offset = 5
        self._circle_size = 2

        self._draw_contour = False
        self._draw_ellipse = True
        self._draw_line = True
        self._lx1 = 0
        self._ly1 = 0
        self._lx2 = 0
        self._ly2 = 0
        self._travel_route_draw_amount = 200
        self._draw_travel_orientation = True
        self._draw_travel_route = True
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

        self.lx1 = int(round(center_x - self.lineend_offset*x_dif))
        self.ly1 = int(round(center_y - self.lineend_offset*y_dif))
        self.lx2 = int(round(center_x + self.lineend_offset*x_dif))
        self.ly2 = int(round(center_y + self.lineend_offset*y_dif))

    # def append_to_travel_orientation(self):
    #     coordinates = (self.lx1, self.ly1, self.lx2, self.ly2)
    #     self.img_travel_orientation.append(coordinates)
    #
    # def append_to_travel_route(self, ellipse):
    #     if not self.draw_travel_route:
    #         return
    #
    #     if ellipse is not None:
    #         ellipse_x = int(round(ellipse[0][0]))
    #         ellipse_y = int(round(ellipse[0][1]))
    #         point = (ellipse_x, ellipse_y)
    #         self.img_travel_route.append(point)

    def draw_preview_img(self, ellipse, data_manager, bool_fish_started, contour_list, roi):
        # draw data for visual feedback while tracking
        if ellipse is not None:
            ellipse = ((ellipse[0][0]+roi.x1, ellipse[0][1]+roi.y1), ellipse[1], ellipse[2])

        # draw ellipse
        if self._draw_ellipse and ellipse is not None and bool_fish_started:
            cv2.ellipse(self.current_frame, ellipse, (0, 0, 255), 2)

        # draw countours to ROI img and show img
        if self.draw_contour and contour_list is not None:
            cv2.drawContours(self.current_frame, contour_list, -1, (0, 255, 0), 3, offset=(roi.x1, roi.y1))

        # draw travel route
        if self.draw_travel_route:
            positions = data_manager.all_pos_original
            for i in range(len(positions)-self._travel_route_draw_amount,  len(positions)):
            # for point in data_manager.all_pos_original:
                if i >= 0 and positions[i] is not None:
                    point = positions[i]
                    cv2.circle(self.current_frame, (int(point[0]), int(point[1])), self._circle_size, (255, 0, 0))

        # draw travel orientation  # needed??
        # if self.draw_travel_orientation:
        #     for coordinates in data_manager.all_pos_original:
        #         if coordinates is not None:
        #             cv2.line(self.current_frame, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), (150,150,0), 1)

    def draw_data_on_overview_image(self, roi, dm):
        # for coordinates in self.dm.:  # needed?
        #     cv2.line(self.overview_output, (coordinates[0] + roi.x1, coordinates[1] + roi.y1),
        #              (coordinates[2] + roi.x1, coordinates[3] + roi.y1), (150,150,0), 1)
        for point in dm.all_pos_original:
            if point is not None:
                cv2.circle(self._overview_output, (int(round(point[0])), int(round(point[1]))), self._circle_size, (255, 0, 0))

    def draw_estimated_data_on_overview_image(self, estimated_pos_roi, roi, circle_size):
        for c in estimated_pos_roi:
            if c is not None:
                cv2.circle(self._overview_output, (int(round(c[0])) + roi.x1, int(round(c[1]) + roi.y1)), circle_size, (0, 0, 255))

    def show_imgs(self):
        cv2.namedWindow("current frame", cv2.WINDOW_NORMAL)
        cv2.imshow("current frame", self.current_frame)
        if self.show_bg_sub_img:
            cv2.namedWindow("bgsub", cv2.WINDOW_NORMAL)
            cv2.imshow("bgsub", self._current_bg_sub)
        if self.show_morphed_img:
            cv2.namedWindow("morphed_bgsub", cv2.WINDOW_NORMAL)
            cv2.imshow("morphed_bgsub", self._current_morphed)
        return

    def import_cfg_values(self, cfg):
        self.show_bg_sub_img = cfg.getboolean('image_processing', 'show_bg_sub_img')
        self.show_morphed_img = cfg.getboolean('image_processing', 'show_morphed_img')
        self.draw_contour = cfg.getboolean('image_processing', 'draw_contour')
        self.draw_ellipse = cfg.getboolean('image_processing', 'draw_ellipse')

        self.lineend_offset = cfg.getint('visualization', 'lineend_offset')
        self.circle_size = cfg.getint('visualization', 'circle_size')

    def add_cfg_values(self, cfg):
        cfg.add_section('image_processing')
        cfg.set('image_processing', 'show_bg_sub_img', str(self.show_bg_sub_img))
        cfg.set('image_processing', 'show_morphed_img', str(self.show_morphed_img))
        cfg.set('image_processing', 'draw_contour', str(self.draw_contour))
        cfg.set('image_processing', 'draw_ellipse', str(self.draw_ellipse))
        cfg.add_section('visualization')
        cfg.set('visualization', 'lineend_offset', str(self.lineend_offset))
        cfg.set('visualization', 'circle_size', str(self.circle_size))

    @property
    def current_frame(self):
        return self._current_frame
    @current_frame.setter
    def current_frame(self, frame):
        self._current_frame = frame

    @property
    def current_bg_sub(self):
        return self._current_bg_sub
    @current_bg_sub.setter
    def current_bg_sub(self, img):
        self._current_bg_sub = img

    @property
    def current_morphed(self):
        return self._current_morphed
    @current_morphed.setter
    def current_morphed(self, img):
        self._current_morphed = img

    @property
    def overview_output(self):
        return self._overview_output
    @overview_output.setter
    def overview_output(self, frame):
        self._overview_output = frame

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