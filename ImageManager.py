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
        self._lx1 = 0
        self._ly1 = 0
        self._lx2 = 0
        self._ly2 = 0
        self._draw_travel_orientation = True
        self._draw_travel_route = True
        self._draw_original_output = True
        self._show_bg_sub_img = False
        self._show_morphed_img = False

    def append_to_travel_orientation(self):
        coordinates = (self.lx1, self.ly1, self.lx2, self.ly2)
        self.img_travel_orientation.append(coordinates)

    def append_to_travel_route(self, ellipse):
        if ellipse is not None:
            ellipse_x = int(round(ellipse[0][0]))
            ellipse_y = int(round(ellipse[0][1]))
            point = (ellipse_x, ellipse_y)
            self.img_travel_route.append(point)

    # TODO create this to draw all the data and only call this function in Tracker.extract_dat()!
    def draw_extracted_data(self):
        return

    # FIXME estimated data not visible anymore after merging with real data!
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