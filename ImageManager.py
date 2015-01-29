import cv2

class ImageManager(object):

    def __init__(self):
        self._img_travel_orientation = []
        self._img_travel_route = []

        self._last_frame = None
        self._last_frame_ov_output = None

        self._draw_contour = False
        self._draw_ellipse = True
        self._draw_line = True
        self._draw_travel_orientation = True
        self._draw_travel_route = True
        self._draw_original_output = True
        self._show_bg_sub_img = False
        self._show_morphed_img = False

    def append_to_travel_orientation(self):
        coordinates = (self.lx1, self.ly1, self.lx2, self.ly2)
        self.img_travel_orientation.append(coordinates)

    def append_to_travel_route(self):
        if self.ellipse is not None:
            ellipse_x = int(round(self.ellipse[0][0]))
            ellipse_y = int(round(self.ellipse[0][1]))
            point = (ellipse_x, ellipse_y)
            self.img_travel_route.append(point)

    def draw_extracted_date(self):

        return

    def draw_estimated_data(self):
        if not self.estimate_missing_data:
            return

        for c in self.dm.estimated_pos_roi:
            if c is not None:
                cv2.circle(self.last_frame, (int(round(c[0])), int(round(c[1]))), self._circle_size, (0, 0, 255))
                cv2.circle(self.last_frame_OV_output, (int(round(c[0])) + self.roi.x1, int(round(c[1]) + self.roi.y1)), self._circle_size, (0, 0, 255))





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