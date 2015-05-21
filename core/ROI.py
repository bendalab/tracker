import numpy as np


class ROI(object):
    def __init__(self, x_1, y_1, x_2, y_2, name):
        self._name = name
        self._x_1 = x_1
        self._y_1 = y_1
        self._x_2 = x_2
        self._y_2 = y_2

        self._frame_data = {}
        self._frame_data["mean_colors"] = []

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
            print "values imported for roi: {0:s}".format(self.name)
        except:
            print "no values in config for roi: {0:s}".format(self.name)
            return

    def calc_mean_color(self, img):
        img_roi = img[self.y1:self.y2, self.x1:self.x2]
        mean_color = tuple([int(entry) for entry in np.mean(np.mean(img_roi, 0), 0)])
        self._frame_data["mean_colors"].append(mean_color)
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

# debug main
# if __name__ == "__main__":
#     import cv2
#     img = cv2.imread("/home/madai/Pictures/two_color.png")
#     roi1 = ROI(0, 0, 300, 400, "roi1")
#     roi2 = ROI(0, 0, 400, 400, "roi2")
#
#     roi1.calc_mean_color(img)
#     roi2.calc_mean_color(img)
#
#     print roi1.mean_color
#     print roi2.mean_color
