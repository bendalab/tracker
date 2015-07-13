import numpy as np
import cv2


class ROI(object):
    def __init__(self, x_1, y_1, x_2, y_2, name):
        self._name = name
        self._x_1 = x_1
        self._y_1 = y_1
        self._x_2 = x_2
        self._y_2 = y_2

        self._frame_data = {}
        self._frame_data["{0:s}_mean_colors".format(self._name)] = []

    def set_values(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_values(self):
        return self.x1, self.y1, self.x2, self.y2

    def import_cfg_values(self, cfg):
        try:
            section = 'roi_{0:s}'.format(self.name)
            self.x1 = cfg.getint(section, "x1")
            self.x2 = cfg.getint(section, "x2")
            self.y1 = cfg.getint(section, "y1")
            self.y2 = cfg.getint(section, "y2")
        except:
            print "New roi: {0:s}; no values in config.".format(self.name)
            return

    def check_and_adjust_values(self, cap):
        width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        if self._x_1 < 0:
            self._x_1 = 0
        if self._x_1 > width:
            self._x_1 = int(width-2)
        if self._x_2 < 0:
            self._x_2 = 2
        if self._x_2 > width:
            self._x_2 = int(width-1)
        if self._y_1 < 0:
            self._y_1 = 0
        if self._y_1 > height:
            self._y_1 = int(height-2)
        if self._y_2 < 0:
            self._y_2 = 2
        if self._y_2 > height:
            self._y_2 = int(height-1)

    def calc_mean_color(self, img):
        img_roi = img[self._y_1:self._y_2, self._x_1:self._x_2]
        mean_color = tuple([int(entry) for entry in np.mean(np.mean(img_roi, 0), 0)])
        self._frame_data["{0:s}_mean_colors".format(self._name)].append(mean_color)
        return

    def calc_all_data(self, img):
        # implemented to allow adding of more properties later
        self.calc_mean_color(img)

    @property
    def name(self):
        return self._name

    @property
    def frame_data(self):
        return self._frame_data

    @property
    def x1(self):
        return self._x_1

    @x1.setter
    def x1(self, value):
        self._x_1 = value

    @property
    def y1(self):
        return self._y_1

    @y1.setter
    def y1(self, value):
        self._y_1 = value

    @property
    def x2(self):
        return self._x_2

    @x2.setter
    def x2(self, value):
        self._x_2 = value

    @property
    def y2(self):
        return self._y_2

    @y2.setter
    def y2(self, value):
        self._y_2 = value

#debug main
if __name__ == "__main__":
    import cv2
    img = cv2.imread("/home/madai/Pictures/two_color.png")
    roi1 = ROI(0, 0, 300, 400, "roi1")
    roi2 = ROI(0, 0, 400, 400, "roi2")

    roi1.calc_all_data(img)
    roi2.calc_all_data(img)
    roi1.calc_all_data(img)
    roi2.calc_all_data(img)

    print roi1.frame_data
    print roi2.frame_data
