class RelROI(object):
    def __init__(self, x1_factor, y1_factor, x2_factor, y2_factor):
        self._x1_factor = x1_factor
        self._x2_factor = x2_factor
        self._y1_factor = y1_factor
        self._y2_factor = y2_factor

    @property
    def x1_factor(self):
        return self._x1_factor
    @x1_factor.setter
    def x1_factor(self, value):
        self._x1_factor = value

    @property
    def x2_factor(self):
        return self._x2_factor
    @x2_factor.setter
    def x2_factor(self, value):
        self._x2_factor = value

    @property
    def y1_factor(self):
        return self._y1_factor
    @y1_factor.setter
    def y1_factor(self, value):
        self._y1_factor = value

    @property
    def y2_factor(self):
        return self._y2_factor
    @y2_factor.setter
    def y2_factor(self, value):
        self._y2_factor = value