class ROI(object):
    def __init__(self, x_1, y_1, x_2, y_2, name):
        self._name = name
        self._x_1 = x_1
        self._y_1 = y_1
        self._x_2 = x_2
        self._y_2 = y_2

        self.mean_color = None

    def set_values(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_values(self):
        return self.x1, self.y1, self.x2, self.y2

    def import_cfg_values(self, cfg):
        section = 'roi_{0:s}'.format(self.name)
        self.x1 = cfg.getint(section, "x1")
        self.x2 = cfg.getint(section, "x2")
        self.y1 = cfg.getint(section, "y1")
        self.y2 = cfg.getint(section, "y2")

    @property
    def name(self):
        return self._name

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
